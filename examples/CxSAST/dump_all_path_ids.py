"""Dump all path_ids from a scan's SAST results.

Uses get_all_scan_results which handles the page-based offset semantics
of /cxrestapi/sast/results correctly.

Usage:
    PYTHONPATH=. python scripts/dump_all_path_ids.py

Requires a CxSAST config in ~/.Checkmarx/config.ini or environment
variables prefixed with cxsast_ (e.g. cxsast_base_url, cxsast_username).
"""
import os
from pathlib import Path

# Load .env if present
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ[key.strip()] = value.strip().strip("\"'")

from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI, ScansAPI


def main():
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()

    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(
        "jvl_git", "/CxServer"
    )
    scan_id = scan_api.get_last_scan_id_of_a_project(
        project_id,
        only_finished_scans=True,
        only_completed_scans=True,
        only_real_scans=True,
        only_full_scans=True,
    )
    if not scan_id:
        print("No qualifying scan found.")
        return

    results = scan_api.get_all_scan_results(scan_id=scan_id, limit=20)
    path_ids = [r.path_id for r in results]
    unique = len(set(path_ids))

    print(f"Scan ID: {scan_id}")
    print(f"Total fetched: {len(results)}")
    print(f"Unique:        {unique}")
    print(f"Duplicates:    {len(results) - unique}")

    print(f"\n--- All {len(path_ids)} path_ids ---")
    for pid in path_ids:
        print(pid)


if __name__ == "__main__":
    main()
