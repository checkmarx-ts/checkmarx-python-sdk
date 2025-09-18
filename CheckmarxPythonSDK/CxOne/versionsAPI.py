from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne.dto import (
    VersionsOut, construct_versions_out
)
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT

api_url = "/api/versions"


class VersionsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_versions_from_engines(self) -> VersionsOut:
        """

        Returns:
            VersionsOut
        """
        relative_url = f"{api_url}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_versions_out(item)
