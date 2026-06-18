"""
Get the last scan on the main branch for every project, retrieve all SAST
results, and export counts broken down by project AND query.

Output CSV headers:
    project_name, query_name, severity, language, to_verify, confirmed,
    urgent, not_exploitable, proposed_not_exploitable

Secrets are read from a .env file in the project root.

Usage:
    python export_sast_state_by_query.py
"""

import csv
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.sastResultsAPI import SastResultsAPI

OUTPUT_CSV = Path(__file__).resolve().parent / "sast_state_by_query_v6.csv"
STATES = ["TO_VERIFY", "CONFIRMED", "URGENT",
           "NOT_EXPLOITABLE", "PROPOSED_NOT_EXPLOITABLE"]


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


def fetch_all_sast_results(sast_api: SastResultsAPI, scan_id: str):
    """Paginate through all SAST results for a scan. Returns list of SastResult."""
    all_results = []
    offset = 0
    limit = 1000
    while True:
        result = sast_api.get_sast_results_by_scan_id(
            scan_id=scan_id, include_nodes=False, offset=offset, limit=limit,
        )
        batch = result.get("results", [])
        all_results.extend(batch)
        total = result.get("totalCount", 0)
        if offset + limit >= total:
            break
        offset += limit
    return all_results


def main():
    configuration = build_configuration()
    api_client = ApiClient(configuration=configuration)

    projects_api = ProjectsAPI(api_client=api_client)
    sast_api = SastResultsAPI(api_client=api_client)

    all_projects = projects_api.get_all_projects()
    print(f"Found {len(all_projects)} projects.")

    project_lookup = {p.id: p for p in all_projects}
    project_ids = [p.id for p in all_projects]

    last_scans = projects_api.get_last_scan_info(
        project_ids=project_ids, use_main_branch=True, limit=100,
    )
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)

    # filter to scans within the cutoff window
    recent_scans = {}
    skipped_old = 0
    for pid, scan in last_scans.items():
        if not scan or not scan.created_at:
            skipped_old += 1
            continue
        try:
            created = datetime.fromisoformat(scan.created_at.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            skipped_old += 1
            continue
        if created >= cutoff:
            recent_scans[pid] = scan
        else:
            skipped_old += 1
    print(f"Projects with a last scan on main branch: {len(last_scans)}"
          f" ({len(recent_scans)} within 2 days, {skipped_old} older)")

    headers = [
        "project_name", "query_name", "severity", "language",
        "to_verify", "confirmed", "urgent",
        "not_exploitable", "proposed_not_exploitable",
    ]

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        total = len(recent_scans)
        for i, (pid, scan) in enumerate(recent_scans.items(), 1):
            project = project_lookup.get(pid)
            if not scan or not project:
                continue
            name = project.name
            scan_id = scan.id

            print(f"  [{i}/{total}] {name} ...", end=" ", flush=True)

            results = fetch_all_sast_results(sast_api, scan_id)
            # count by (query_name, state); capture query-level attributes
            state_counters = defaultdict(lambda: defaultdict(int))
            query_severity = {}
            query_language = {}
            for r in results:
                query = r.query_name or "(unknown)"
                state = r.state or "TO_VERIFY"
                if state not in STATES:
                    state = "TO_VERIFY"
                state_counters[query][state] += 1
                if query not in query_severity:
                    sev = (r.severity or "").upper()
                    query_severity[query] = sev
                if query not in query_language:
                    lang = r.language_name or ""
                    query_language[query] = lang

            print(f"{len(results)} results, {len(state_counters)} queries")

            for query in sorted(state_counters):
                s = state_counters[query]
                writer.writerow({
                    "project_name": name,
                    "query_name": query,
                    "severity": query_severity.get(query, ""),
                    "language": query_language.get(query, ""),
                    "to_verify": s.get("TO_VERIFY", 0),
                    "confirmed": s.get("CONFIRMED", 0),
                    "urgent": s.get("URGENT", 0),
                    "not_exploitable": s.get("NOT_EXPLOITABLE", 0),
                    "proposed_not_exploitable": s.get("PROPOSED_NOT_EXPLOITABLE", 0),
                })

    print(f"\nWrote to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
