from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class SastResultsCompareAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/scans-compare/sast"
        )

    def get_compare_status(
        self, scan_id: str, base_scan_id: str
    ) -> dict:
        """
        Get total counts of results per severity and status for two scans.

        Args:
            scan_id (str): Scan ID of the newer scan
            base_scan_id (str): Scan ID of the older scan

        Returns:
            dict with severityStatusCounters, scanCounters, baseScanCounters
        """
        url = f"{self.base_url}/status"
        params = {"scan-id": scan_id, "base-scan-id": base_scan_id}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


# ---- Module-level convenience function ----

def get_compare_status(scan_id: str, base_scan_id: str) -> dict:
    return SastResultsCompareAPI().get_compare_status(
        scan_id=scan_id, base_scan_id=base_scan_id,
    )
