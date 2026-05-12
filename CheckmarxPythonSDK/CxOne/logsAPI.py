from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class LogsAPI(object):
    """Logs API client for retrieving scan logs."""

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/logs"
        )

    def get_log(self, scan_id: str, scan_type: str) -> str:
        """
        Get log file content for a specific scan.

        Args:
            scan_id (str): The unique identifier of the scan
            scan_type (str): The type of the scan

        Returns:
            str: The log file content
        """
        url = f"{self.base_url}/{scan_id}/{scan_type}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.text


def get_log(scan_id: str, scan_type: str) -> str:
    """
    Convenience function to get log file content.

    Args:
        scan_id (str): The unique identifier of the scan
        scan_type (str): The type of the scan

    Returns:
        str: The log file content
    """
    return LogsAPI().get_log(scan_id=scan_id, scan_type=scan_type)
