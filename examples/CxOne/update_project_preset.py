"""
Get the SAST "presetName" parameter for projects listed in a CSV file.
Print it, update it, then print it again.

Secrets are read from a .env file in the project root.

CSV file format (project_to_be_update_preset.csv):
    Project Name,Risk Level,Application,Rationale

Usage:
    python update_project_preset.py

.env file format:
    CXONE_TENANT_NAME=your-tenant
    CXONE_CLIENT_ID=ast-app
    CXONE_CLIENT_SECRET=your-client-secret
    CXONE_REFRESH_TOKEN=your-refresh-token
"""

import csv
import os
from pathlib import Path

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.scanConfigurationAPI import ScanConfigurationAPI
from CheckmarxPythonSDK.CxOne.dto.ScanParameter import ScanParameter

PRESET_KEY = "scan.config.sast.presetName"
CSV_FILE = Path(__file__).resolve().parent / "project_to_be_update_preset.csv"
NEW_PRESET_NAME = "OWASP TOP 10 API 2023 - TMCA"


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
    access_control_url = os.environ.get("CXONE_IAM_URL", "https://sng.iam.checkmarx.net")
    server_base_url = os.environ.get("CXONE_SERVER_URL", "https://sng.ast.checkmarx.net")
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


def load_target_project_names():
    """Read project names from the CSV file."""
    if not CSV_FILE.exists():
        print(f"Error: {CSV_FILE} not found.")
        return []
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        return [row["Project Name"].strip() for row in reader if row.get("Project Name", "").strip()]


def get_preset_param(api: ScanConfigurationAPI, project_id: str):
    parameters = api.get_the_list_of_all_the_parameters_for_a_project(project_id)
    return next(
        (p for p in parameters if p.key == PRESET_KEY), None
    )


def main():
    target_names = load_target_project_names()
    if not target_names:
        print("No project names found in CSV file.")
        return
    print(f"Loaded {len(target_names)} project name(s) from {CSV_FILE.name}.\n")

    configuration = build_configuration()
    api_client = ApiClient(configuration=configuration)

    projects_api = ProjectsAPI(api_client=api_client)
    scan_config_api = ScanConfigurationAPI(api_client=api_client)

    all_projects = projects_api.get_all_projects()
    projects = [p for p in all_projects if p.name in target_names]
    if not projects:
        print(f"No target projects found among {len(all_projects)} total projects.")
        return
    print(f"Found {len(projects)} target project(s) out of {len(all_projects)} total.\n")

    # Step 1: Get current preset for target projects
    print("=" * 60)
    print("Step 1: Get current project preset")
    print("=" * 60)
    for project in projects:
        param = get_preset_param(scan_config_api, project.id)
        value = param.value if param else "N/A"
        value_display = value if value != "" else "(empty)"
        print(f"  {project.name}: {value_display}")

    # Step 2: Update preset for target projects
    print(f"\n{'=' * 60}")
    print("Step 2: Update project preset")
    print(f"{'=' * 60}")
    for project in projects:
        update_param = ScanParameter(
            key=PRESET_KEY,
            value=NEW_PRESET_NAME,
            valueType="String",
            allowOverride=True,
        )
        success = scan_config_api.define_parameters_in_the_input_list_for_a_specific_project(
            project_id=project.id,
            scan_parameters=[update_param],
        )
        status = "OK" if success else "FAILED"
        print(f"  {project.name}: {status}")

    # Step 3: Verify preset for target projects
    print(f"\n{'=' * 60}")
    print("Step 3: Verify project preset")
    print(f"{'=' * 60}")
    for project in projects:
        param = get_preset_param(scan_config_api, project.id)
        value = param.value if param else "N/A"
        value_display = value if value != "" else "(empty)"
        print(f"  {project.name}: {value_display}")


if __name__ == "__main__":
    main()
