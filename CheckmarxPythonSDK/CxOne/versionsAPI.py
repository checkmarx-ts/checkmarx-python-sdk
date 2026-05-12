from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne.dto import VersionsOut


class VersionsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/versions"
        )

    def get_versions_from_engines(self) -> VersionsOut:
        """
        Get versions from engines.

        Returns:
            VersionsOut
        """
        response = self.api_client.call_api(
            method="GET", url=self.base_url
        )
        return VersionsOut.from_dict(response.json())


def get_versions_from_engines() -> VersionsOut:
    return VersionsAPI().get_versions_from_engines()
