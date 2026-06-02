from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class KicsMetadataAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/kics-metadata"
        )

    def get_kics_scans_metadata(self, scan_ids: List[str]) -> dict:
        """
        Get KICS scan metadata for multiple scan IDs.

        Args:
            scan_ids (List[str]): List of scan UUIDs

        Returns:
            dict with totalCount, scans, missing
        """
        url = f"{self.base_url}/"
        params = {"scan-ids": scan_ids}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_kics_scan_metadata(self, scan_id: str) -> dict:
        """
        Get KICS scan metadata for a single scan.

        Args:
            scan_id (str): Scan UUID

        Returns:
            dict with scanId, projectId, loc, kicsLoc, fileCount
        """
        url = f"{self.base_url}/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()


# ---- Module-level convenience functions ----

def get_kics_scans_metadata(scan_ids: List[str]) -> dict:
    return KicsMetadataAPI().get_kics_scans_metadata(scan_ids=scan_ids)


def get_kics_scan_metadata(scan_id: str) -> dict:
    return KicsMetadataAPI().get_kics_scan_metadata(scan_id=scan_id)
