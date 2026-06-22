"""
Trigger scans on the main branch for projects with Code Repository
integration (SCM-managed projects), using the repos-manager projectScan
endpoint.

Secrets are read from a .env file in the project root.

Usage:
    python trigger_scm_project_scans_on_main_branch.py

.env file format:
    CXONE_TENANT_NAME=your-tenant
    CXONE_CLIENT_ID=ast-app
    CXONE_CLIENT_SECRET=your-client-secret
    CXONE_REFRESH_TOKEN=your-refresh-token
"""

import os
import re
from pathlib import Path

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.repoManagerAPI import RepoManagerAPI


def load_dotenv():
    """Load .env file from the project root."""
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


def parse_scm_info(repo_url):
    """Extract origin and organization from a repo URL."""
    if not repo_url:
        return None, None
    match = re.search(r"://(?:www\.)?([^.]+)\.(?:com|org)/([^/]+)", repo_url)
    if not match:
        return None, None
    origin = match.group(1).upper()
    organization = match.group(2)
    return origin, organization


def main():
    configuration = build_configuration()
    api_client = ApiClient(configuration=configuration)

    projects_api = ProjectsAPI(api_client=api_client)
    repo_manager_api = RepoManagerAPI(api_client=api_client)

    project_list = projects_api.get_all_projects()
    print(f"Found {len(project_list)} projects.\n")

    skipped = []
    scanned = []
    failed = []

    for project_summary in project_list:
        project = projects_api.get_a_project_by_id(project_summary.id)
        repo_id = project.repo_id
        scm_repo_id = project.scm_repo_id
        repo_url = project.repo_url
        main_branch = project.main_branch

        if not repo_id:
            skipped.append((project.name, "no repo_id (SCM not connected)"))
            continue
        if not scm_repo_id:
            skipped.append((project.name, "no scm_repo_id"))
            continue
        if not main_branch:
            skipped.append((project.name, "no main_branch"))
            continue

        # fallback: fetch repo_url from repo-manager if not on the project
        if not repo_url:
            try:
                repo = repo_manager_api.get_repo_by_id(repo_id)
                repo_url = repo.get("url", "")
            except Exception:
                pass
        if not repo_url:
            skipped.append((project.name, "no repo_url"))
            continue

        origin, organization = parse_scm_info(repo_url)
        if not origin or not organization:
            skipped.append((project.name, f"cannot parse origin/org from repo_url: {repo_url}"))
            continue

        repo_identity = scm_repo_id if scm_repo_id else repo_url.rstrip("/").split("/")[-1]

        print(
            f"  {project.name}: "
            f"origin={origin}, org={organization}, "
            f"repo_id={repo_id}, branch={main_branch}",
            end=""
        )

        try:
            result = repo_manager_api.scm_managed_project_scan(
                project_id=project.id,
                origin=origin,
                organization=organization,
                repo_id=repo_id,
                repo_identity=repo_identity,
                repo_url=repo_url,
                default_branch=main_branch,
            )
            if result.status_code in (200, 201, 202):
                print(" -> OK")
                scanned.append((project.name, "OK"))
            else:
                print(f" -> FAILED (status={result.status_code})")
                failed.append((project.name, f"status={result.status_code}"))
        except Exception as e:
            print(f" -> FAILED: {e}")
            failed.append((project.name, str(e)))

    print(f"\n{'=' * 60}")
    print(f"Summary: {len(project_list)} total")
    print(f"  Scanned: {len(scanned)}")
    print(f"  Skipped: {len(skipped)}")
    print(f"  Failed:  {len(failed)}")

    if skipped:
        print(f"\nSkipped:")
        for name, reason in skipped:
            print(f"  {name}: {reason}")
    if failed:
        print(f"\nFailed:")
        for name, error in failed:
            print(f"  {name}: {error}")


if __name__ == "__main__":
    main()
