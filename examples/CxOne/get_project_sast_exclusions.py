"""
Get SAST engine "recommended exclusions" parameter for ALL projects.
If false/empty, set it to true, then verify.

Secrets are read from a .env file in the project root.

Usage:
    python get_project_sast_exclusions.py

.env file format:
    CXONE_TENANT_NAME=your-tenant
    CXONE_CLIENT_ID=ast-app
    CXONE_CLIENT_SECRET=your-client-secret
    CXONE_REFRESH_TOKEN=your-refresh-token
"""

import os
from pathlib import Path

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.scanConfigurationAPI import ScanConfigurationAPI
from CheckmarxPythonSDK.CxOne.dto.ScanParameter import ScanParameter

RECOMMENDED_EXCLUSIONS_KEY = "scan.config.sast.recommendedExclusions"


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
    access_control_url = os.environ.get("CXONE_IAM_URL", "https://iam.checkmarx.net")
    server_base_url = os.environ.get("CXONE_SERVER_URL", "https://ast.checkmarx.net")
    grant_type = os.environ.get("CXONE_GRANT_TYPE", "refresh_token")
    client_id = os.environ.get("CXONE_CLIENT_ID", "ast-app")
    client_secret = os.environ.get("CXONE_CLIENT_SECRET")
    refresh_token = os.environ.get("CXONE_REFRESH_TOKEN")
    # fallback: client_credentials
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


def get_exclusion_param(api: ScanConfigurationAPI, project_id: str):
    parameters = api.get_the_list_of_all_the_parameters_for_a_project(project_id)
    return next(
        (p for p in parameters if p.key == RECOMMENDED_EXCLUSIONS_KEY), None
    )


def is_false_or_empty(param):
    if param is None:
        return True
    value = (param.value or "").strip().lower()
    return value in ("", "false")


def main():
    configuration = build_configuration()
    api_client = ApiClient(configuration=configuration)

    projects_api = ProjectsAPI(api_client=api_client)
    scan_config_api = ScanConfigurationAPI(api_client=api_client)

    projects = projects_api.get_all_projects()
    print(f"Found {len(projects)} projects.\n")

    # Step 1: Check all projects
    print("=" * 60)
    print("Step 1: Check all projects")
    print("=" * 60)
    needs_update = []
    for project in projects:
        param = get_exclusion_param(scan_config_api, project.id)
        value = param.value if param else "N/A"
        value_display = value if value != "" else "(empty)"
        print(f"  {project.name}: {value_display}")
        if is_false_or_empty(param):
            needs_update.append(project)

    # Step 2: Update projects that are false/empty
    if needs_update:
        print(f"\n{'=' * 60}")
        print(f"Step 2: Set to true for {len(needs_update)} project(s)")
        print(f"{'=' * 60}")
        for project in needs_update:
            update_param = ScanParameter(
                key=RECOMMENDED_EXCLUSIONS_KEY,
                value="true",
                valueType="Bool",
                allowOverride=True,
            )
            success = scan_config_api.define_parameters_in_the_input_list_for_a_specific_project(
                project_id=project.id,
                scan_parameters=[update_param],
            )
            status = "OK" if success else "FAILED"
            print(f"  {project.name}: {status}")
    else:
        print("\nNo projects need updating.")

    # Step 3: Verify all projects again
    print(f"\n{'=' * 60}")
    print("Step 3: Verify all projects")
    print(f"{'=' * 60}")
    for project in projects:
        param = get_exclusion_param(scan_config_api, project.id)
        value = param.value if param else "N/A"
        value_display = value if value != "" else "(empty)"
        print(f"  {project.name}: {value_display}")


if __name__ == "__main__":
    main()
