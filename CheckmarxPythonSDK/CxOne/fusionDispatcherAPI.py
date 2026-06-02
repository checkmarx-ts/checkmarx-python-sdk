from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class FusionDispatcherAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/correlation/dispatcher"
        )

    def correlate(self, id: str) -> bool:
        """
        Request starting a new fusion scan for an application.

        Args:
            id (str): Application ID (uuid)

        Returns:
            bool — True if the scan was triggered (HTTP 201)
        """
        url = f"{self.base_url}/{id}/correlate"
        response = self.api_client.call_api(method="POST", url=url)
        return response.status_code == 201

    def get_scan_status(self, id: str) -> dict:
        """
        Get the status of the latest fusion scan for an application.

        Args:
            id (str): Application ID (uuid)

        Returns:
            dict with tenantId, applicationId, scanId, scanStatus,
            stage, stageDescription, scanTimestamp, errorMessage
        """
        url = f"{self.base_url}/{id}/scan-status"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()


# ---- Module-level convenience functions ----

def correlate(id: str) -> bool:
    return FusionDispatcherAPI().correlate(id=id)


def get_scan_status(id: str) -> dict:
    return FusionDispatcherAPI().get_scan_status(id=id)
