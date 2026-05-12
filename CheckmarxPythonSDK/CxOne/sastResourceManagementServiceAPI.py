from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import SastScan, Property
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT


class SastResourceManagementServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/sast-rm"
        )

    def get_sast_scan_allocation_info(self, scan_id) -> SastScan:
        """
        Args:
            scan_id (str):

        Returns:
            SastScan
        """
        url = f"{self.base_url}/scans/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return SastScan.from_dict(response.json())

    def delete_sast_scan(self, scan_id: str) -> bool:
        """
        Args:
            scan_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/scans/{scan_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def get_sast_scans(
        self,
        offset: int = 0,
        limit: int = 20,
        ids: List[str] = None,
        with_deleted: bool = None,
    ) -> dict:
        """
        Args:
            offset (int): Items to skip before collecting the result set.
            limit (int): Number of items to return.
            ids (list of str): Ids of scans to return.
            with_deleted (bool): Whether to include deleted scans.

        Returns:
            dict
        """
        url = f"{self.base_url}/scans"
        params = {
            "offset": offset,
            "limit": limit,
            "ids": ids,
            "with-deleted": with_deleted,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        item = response.json()
        return {
            "totalCount": item.get("totalCount", 0),
            "scans": [
                SastScan.from_dict(scan)
                for scan in (item.get("scans") or [])
            ],
        }


def get_sast_scan_allocation_info(scan_id) -> SastScan:
    return SastResourceManagementServiceAPI().get_sast_scan_allocation_info(
        scan_id=scan_id
    )


def delete_sast_scan(scan_id: str) -> bool:
    return SastResourceManagementServiceAPI().delete_sast_scan(
        scan_id=scan_id
    )


def get_sast_scans(
    offset: int = 0,
    limit: int = 20,
    ids: List[str] = None,
    with_deleted: bool = None,
) -> dict:
    return SastResourceManagementServiceAPI().get_sast_scans(
        offset=offset, limit=limit, ids=ids, with_deleted=with_deleted
    )
