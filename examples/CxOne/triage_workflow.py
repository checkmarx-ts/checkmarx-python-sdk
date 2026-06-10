"""
Guided triage workflow for SAST findings in a scan.

Given a project name:
  1. Get the last scan on the main branch
  2. Get SAST scan summary (aggregate by language)
  3-N. For each SAST result:
    3. Get result with full details
    4. Get the query description
    5. Get triage info (predicates) — skip if already triaged by cxservice
    6. Get source file for review
    7. Decision: CONFIRMED / NOT_EXPLOITABLE / Skip
    8. Apply the triage
    9. Verify

Secrets are read from a .env file in the project root.

Usage:
    python triage_workflow.py <project_name>

Example:
    python triage_workflow.py "happy-cook/WebGoat"
"""

import os
import sys
from pathlib import Path

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.sastResultsSummaryAPI import SastResultsSummaryAPI
from CheckmarxPythonSDK.CxOne.sastResultsAPI import SastResultsAPI
from CheckmarxPythonSDK.CxOne.sastQueriesAPI import SastQueriesAPI
from CheckmarxPythonSDK.CxOne.sastResultsPredicatesAPI import SastResultsPredicatesAPI
from CheckmarxPythonSDK.CxOne.repoStoreServiceAPI import RepoStoreServiceAPI

SKIP_USER = "cxservice_happy.yang@checkmarx.com"


def load_dotenv():
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        print(f"Warning: {env_path} not found, using environment variables.")
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("\"'")
            os.environ[key] = value


def build_configuration() -> Configuration:
    load_dotenv()
    tenant_name = os.environ["CXONE_TENANT_NAME"]
    access_control_url = os.environ.get(
        "CXONE_IAM_URL", "https://sng.iam.checkmarx.net"
    )
    server_base_url = os.environ.get(
        "CXONE_SERVER_URL", "https://sng.ast.checkmarx.net"
    )
    grant_type = os.environ.get("CXONE_GRANT_TYPE", "refresh_token")
    client_id = os.environ.get("CXONE_CLIENT_ID", "ast-app")
    client_secret = os.environ.get("CXONE_CLIENT_SECRET")
    refresh_token = os.environ.get("CXONE_REFRESH_TOKEN")
    if not refresh_token:
        grant_type = "client_credentials"
    return Configuration(
        server_base_url=server_base_url,
        iam_base_url=access_control_url,
        token_url=(
            f"{access_control_url}/auth/realms"
            f"/{tenant_name}/protocol/openid-connect/token"
        ),
        tenant_name=tenant_name,
        grant_type=grant_type,
        client_id=client_id,
        client_secret=client_secret,
        api_key=refresh_token,
    )


def find_project_by_name(api: ProjectsAPI, name: str) -> dict:
    project_id = api.get_project_id_by_name(name)
    if not project_id:
        return None
    p = api.get_a_project_by_id(project_id)
    return {"id": p.id, "name": p.name, "mainBranch": p.main_branch}


def get_last_main_branch_scan(api: ProjectsAPI, project_id: str) -> dict:
    scans = api.get_last_scan_info(
        project_ids=[project_id], use_main_branch=True, limit=1,
    )
    scan = scans.get(project_id)
    if not scan:
        return None
    return {"id": scan.id, "createdAt": scan.created_at, "status": scan.status}


def fetch_all_results(results_api: SastResultsAPI, scan_id: str):
    """Paginate through all SAST results. Returns list of SastResult."""
    all_results = []
    offset = 0
    limit = 100
    while True:
        resp = results_api.get_sast_results_by_scan_id(
            scan_id=scan_id,
            include_nodes=True,
            apply_predicates=True,
            offset=offset,
            limit=limit,
            sort=["+status", "+severity", "-queryname"],
        )
        batch = resp.get("results", [])
        all_results.extend(batch)
        total = resp.get("totalCount", 0)
        if offset + limit >= total:
            break
        offset += limit
    return all_results


def get_source_file_info(nodes):
    """Extract source file and line from result nodes."""
    for node in (nodes or []):
        if node.node_type == "source" and node.file_name:
            return node.file_name, node.line
    for node in (nodes or []):
        if node.file_name:
            return node.file_name, node.line
    return None, None


def show_source_code(repostore_api, scan_id, file_path, line_num):
    """Print source code context around the finding line."""
    try:
        code = repostore_api.view_source_code_of_specified_file(
            scan_id=scan_id, file_path=file_path,
        )
        lines = code.split("\n")
        start = max(0, (line_num or 1) - 10)
        end = min(len(lines), (line_num or 1) + 10)
        print(f"  --- Lines {start + 1}-{end} ---")
        for i in range(start, end):
            marker = " >>>" if i == (line_num or 1) - 1 else "    "
            print(f"  {i + 1:4d}{marker} {lines[i]}")
    except Exception as e:
        print(f"  Error reading source: {e}")


def was_triaged_by_cxservice(response):
    """Check if any predicate was created by the skip user.

    Args:
        response: PredicateHistoryResponse from the SDK.
    """
    for proj in (response.predicate_history_per_project or []):
        for pred in (proj.predicates or []):
            if pred.created_by == SKIP_USER:
                return True
    return False


def process_finding(idx, total, finding, project, scan_id,
                    queries_api, predicates_api, repostore_api):
    """Run steps 4-9 for a single SAST finding."""
    similarity_id = str(finding.similarity_id)
    header = f"Finding {idx}/{total} | {finding.query_name} | {finding.severity} | {finding.language_name}"
    print(f"\n{'=' * 70}")
    print(f"{'=' * 70}")
    print(f"  {header}")
    print(f"{'=' * 70}")
    print(f"  Similarity ID: {similarity_id}")
    print(f"  State / Status: {finding.state} / {finding.status}")
    if finding.nodes:
        for node in finding.nodes[:4]:
            print(f"  Node: {node.name} ({node.node_type}) file={node.file_name} line={node.line}")

    # Step 4: Query description
    print(f"\n  --- Step 4: Query description ---")
    try:
        query_desc = queries_api.get_sast_query_description(
            ids=[finding.query_id_str], scan_id=scan_id,
        )
        if query_desc:
            qd = query_desc[0]
            print(f"  Description: {(qd.description or '')[:400]}")
            print(f"  Remediation: {(qd.remediation or '')[:400]}")
    except Exception as e:
        print(f"  Error: {e}")

    # Step 5: Check predicates — skip if already triaged by cxservice
    print(f"\n  --- Step 5: Check predicates ---")
    try:
        predicates = predicates_api.get_all_predicates_for_similarity_id(
            similarity_id=similarity_id,
            project_ids=[project["id"]],
            include_comment_json=True,
            scan_id=scan_id,
        )
    except Exception as e:
        print(f"  Error fetching predicates: {e}")
        return False

    if was_triaged_by_cxservice(predicates):
        print(f"  SKIP: already triaged by {SKIP_USER}")
        return False

    for proj in (predicates.predicate_history_per_project or []):
        for p in (proj.predicates or []):
            print(f"  Pred: {p.state}/{p.severity} by {p.created_by} at {p.created_at}")

    # Step 6: Source file
    print(f"\n  --- Step 6: Source file ---")
    source_file, source_line = get_source_file_info(finding.nodes)
    if source_file:
        print(f"  File: {source_file} (line {source_line})")
        show_source_code(repostore_api, scan_id, source_file, source_line)
    else:
        print("  No source file found.")

    # Step 7: Decision
    print(f"\n  --- Step 7: Decision ---")
    print(f"    1 - CONFIRMED    2 - NOT_EXPLOITABLE    3 - Skip")
    choice = input("  > ").strip()
    if choice not in ("1", "2"):
        print("  Skipped.")
        return False

    new_state = "CONFIRMED" if choice == "1" else "NOT_EXPLOITABLE"
    comment = input(f"  Comment ({new_state}): ").strip()

    # Step 8: Apply triage
    print(f"\n  --- Step 8: Apply triage -> {new_state} ---")
    payload = [{
        "similarityId": similarity_id,
        "projectId": project["id"],
        "scanId": scan_id,
        "allowInconsistentStates": True,
        "state": new_state,
        "comment": comment or f"{new_state} via triage script",
    }]
    try:
        success = predicates_api.predicate_severity_and_state_by_similarity_id_and_project_id(
            data=payload,
        )
        print(f"  Applied: {'OK' if success else 'FAILED'}")
    except Exception as e:
        print(f"  Error: {e}")
        return False

    # Step 9: Verify
    print(f"\n  --- Step 9: Verify ---")
    try:
        latest = predicates_api.get_latest_predicates_for_similarity_id(
            similarity_id=similarity_id,
            project_ids=[project["id"]],
            scan_id=scan_id,
        )
        for proj in (latest.predicate_history_per_project or []):
            for p in (proj.predicates or []):
                print(f"  Latest: {p.state}/{p.severity} by {p.created_by}")
    except Exception as e:
        print(f"  Error: {e}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python triage_workflow.py <project_name>")
        sys.exit(1)
    project_name = sys.argv[1]

    configuration = build_configuration()
    api_client = ApiClient(configuration=configuration)

    projects_api = ProjectsAPI(api_client=api_client)
    summary_api = SastResultsSummaryAPI(api_client=api_client)
    results_api = SastResultsAPI(api_client=api_client)
    queries_api = SastQueriesAPI(api_client=api_client)
    predicates_api = SastResultsPredicatesAPI(api_client=api_client)
    repostore_api = RepoStoreServiceAPI(api_client=api_client)

    # -------- Step 1: Find project & get last scan --------
    print("=" * 70)
    print(f"Step 1: Project '{project_name}'")
    print("=" * 70)
    project = find_project_by_name(projects_api, project_name)
    if not project:
        print(f"  Project '{project_name}' not found.")
        sys.exit(1)
    print(f"  Project ID : {project['id']}")
    print(f"  Main branch: {project['mainBranch']}")

    scan = get_last_main_branch_scan(projects_api, project["id"])
    if not scan:
        print("  No scan found on main branch.")
        sys.exit(1)
    scan_id = scan["id"]
    print(f"  Scan ID    : {scan_id}")
    print(f"  Status     : {scan['status']}")

    # -------- Step 2: SAST summary --------
    print(f"\n{'=' * 70}")
    print(f"Step 2: SAST summary (by LANGUAGE)")
    print(f"{'=' * 70}")
    summary = summary_api.get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=["LANGUAGE"],
        apply_predicates=True,
    )
    if summary.get("scannerSummary"):
        for item in summary["scannerSummary"]:
            lang = item.get("languageName") or item.get("label", "?")
            sev = item.get("severityCounters", {}) or item.get("severity", {})
            print(f"  {lang}: {sev}")
    else:
        print(f"  Raw: {summary}")

    # -------- Step 3: Iterate all SAST results --------
    all_results = fetch_all_results(results_api, scan_id)
    total = len(all_results)
    print(f"\n{'=' * 70}")
    print(f"Step 3: {total} SAST results to triage")
    print(f"{'=' * 70}")
    if not all_results:
        print("  No results found.")
        return

    triaged = 0
    skipped = 0
    
    for i, finding in enumerate(all_results, 1):
        action_taken = process_finding(
            i, total, finding, project, scan_id,
            queries_api, predicates_api, repostore_api,
        )
        if action_taken:
            triaged += 1
        else:
            skipped += 1

    print(f"\n{'=' * 70}")
    print(f"Done: {total} findings, {triaged} triaged, {skipped} skipped")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
