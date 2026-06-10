"""
Get the last scan on the main branch for every project, retrieve SAST
result counts by state, and export a CSV for false-positive-rate analysis.

Output CSV headers:
    project_name, main_branch, scan_id, to_verify, confirmed, urgent,
    not_exploitable, proposed_not_exploitable

Secrets are read from a .env file in the project root.

Usage:
    python export_sast_state_counts.py
"""

import csv
import os
from pathlib import Path

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.sastResultsAPI import SastResultsAPI

OUTPUT_CSV = Path(__file__).resolve().parent / "sast_state_counts.csv"
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


def get_state_counts(sast_api: SastResultsAPI, scan_id: str):
    """Return a dict of {state: count} for one scan."""
    counts = {}
    for state in STATES:
        result = sast_api.get_sast_results_by_scan_id(
            scan_id=scan_id, state=[state], limit=1,
        )
        counts[state] = result.get("totalCount", 0)
    return counts


def main():
    configuration = build_configuration()
    api_client = ApiClient(configuration=configuration)

    projects_api = ProjectsAPI(api_client=api_client)
    sast_api = SastResultsAPI(api_client=api_client)

    # get all projects
    all_projects = projects_api.get_all_projects()
    print(f"Found {len(all_projects)} projects.")

    # build lookup: project_id -> project
    project_lookup = {p.id: p for p in all_projects}

    # get last scan on main branch for all projects
    project_ids = [p.id for p in all_projects]
    last_scans = projects_api.get_last_scan_info(
        project_ids=project_ids, use_main_branch=True, limit=100,
    )
    print(f"Projects with a last scan on main branch: {len(last_scans)}")

    rows = []
    total = len(last_scans)
    for i, (pid, scan) in enumerate(last_scans.items(), 1):
        project = project_lookup.get(pid)
        if not scan or not project:
            continue
        name = project.name
        branch = project.main_branch or scan.branch or ""
        scan_id = scan.id
        print(f"  [{i}/{total}] {name}  scan={scan_id} ...", end=" ")
        counts = get_state_counts(sast_api, scan_id)
        total_issues = sum(counts.values())
        print(f"issues={total_issues}")
        rows.append({
            "project_name": name,
            "main_branch": branch,
            "scan_id": scan_id,
            "to_verify": counts["TO_VERIFY"],
            "confirmed": counts["CONFIRMED"],
            "urgent": counts["URGENT"],
            "not_exploitable": counts["NOT_EXPLOITABLE"],
            "proposed_not_exploitable": counts["PROPOSED_NOT_EXPLOITABLE"],
        })

    # write CSV
    headers = [
        "project_name", "main_branch", "scan_id",
        "to_verify", "confirmed", "urgent",
        "not_exploitable", "proposed_not_exploitable",
    ]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
