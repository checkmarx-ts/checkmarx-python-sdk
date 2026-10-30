from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import CloudConnectionsResponse


class CloudConnectAPI(object):
    """API client for the Integrations Cloud Connect service.

    Manages cloud/vendor connections (e.g. Sysdig, OCI container
    registries -- ECR, GHCR, DockerHub, JFrog) used for runtime cloud
    scanning. Only the list endpoint is currently exposed; it requires
    the "view-runtime-cloud" access management role.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/cloud-connect"
        )

    def get_cloud_connections(
        self, limit: int = 10, offset: int = 0, filter_: str = None
    ) -> CloudConnectionsResponse:
        """GET /connections — list cloud connections, paginated and
        optionally filtered by name.

        Args:
            limit (int, optional): Max results, 1-100. Defaults to 10.
            offset (int, optional): Pagination offset. Defaults to 0.
            filter_ (str, optional): Free-text filter matched against
                the connection name (partial match). (Trailing
                underscore avoids shadowing the built-in `filter`.)

        Returns:
            CloudConnectionsResponse
        """
        params = {"limit": limit, "offset": offset, "filter": filter_}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/connections", params=params,
        )
        return CloudConnectionsResponse.from_dict(response.json())


def get_cloud_connections(
    limit: int = 10, offset: int = 0, filter_: str = None
) -> CloudConnectionsResponse:
    return CloudConnectAPI().get_cloud_connections(
        limit=limit, offset=offset, filter_=filter_,
    )
