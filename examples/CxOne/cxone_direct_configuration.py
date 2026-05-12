"""
Examples showing how to construct Configuration and ApiClient directly,
without relying on a config file or environment variables.
"""

from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.scansAPI import ScansAPI


def make_api_client(
    tenant_name: str,
    grant_type: str,
    refresh_token: str = None,
    client_id: str = None,
    client_secret: str = None,
    access_control_url: str = "https://iam.checkmarx.net",
    server_base_url: str = "https://ast.checkmarx.net",
) -> ApiClient:
    configuration = Configuration(
        server_base_url=server_base_url,
        iam_base_url=access_control_url,
        token_url=(
            f"{access_control_url}/auth/realms"
            f"/{tenant_name}/protocol/openid-connect/token"
        ),
        tenant_name=tenant_name,
        grant_type=grant_type,
        client_id=client_id or "ast-app",
        client_secret=client_secret,
        api_key=refresh_token,
    )
    return ApiClient(configuration=configuration)


# --- Example 1: refresh_token grant type ---
def example_refresh_token():
    api_client = make_api_client(
        tenant_name="my-tenant",
        grant_type="refresh_token",
        refresh_token="<your-refresh-token>",
    )
    projects_api = ProjectsAPI(api_client=api_client)
    scans_api = ScansAPI(api_client=api_client)

    projects = projects_api.get_all_projects()
    print(f"Found {len(projects)} projects")


# --- Example 2: client_credentials grant type ---
def example_client_credentials():
    api_client = make_api_client(
        tenant_name="my-tenant",
        grant_type="client_credentials",
        client_id="<your-client-id>",
        client_secret="<your-client-secret>",
    )
    projects_api = ProjectsAPI(api_client=api_client)

    projects = projects_api.get_all_projects()
    print(f"Found {len(projects)} projects")


# --- Example 3: two tenants simultaneously ---
def example_multi_tenant():
    client_a = make_api_client(
        tenant_name="tenant-a",
        grant_type="refresh_token",
        refresh_token="<refresh-token-a>",
    )
    client_b = make_api_client(
        tenant_name="tenant-b",
        grant_type="refresh_token",
        refresh_token="<refresh-token-b>",
    )

    projects_a = ProjectsAPI(api_client=client_a).get_all_projects()
    projects_b = ProjectsAPI(api_client=client_b).get_all_projects()

    print(f"Tenant A: {len(projects_a)} projects")
    print(f"Tenant B: {len(projects_b)} projects")


if __name__ == "__main__":
    example_refresh_token()
    # example_client_credentials()
    # example_multi_tenant()
