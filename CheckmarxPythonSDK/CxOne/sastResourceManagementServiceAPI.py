from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import SastScan, Property
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT

api_url = "/api/sast-rm"


def construct_sast_scan(item):
    return SastScan(
        scan_id=item.get("id"),
        state=item.get("state"),
        queue_at=item.get("queuedAt"),
        allocated_at=item.get("allocatedAt"),
        running_at=item.get("runningAt"),
        engine=item.get("engine"),
        properties=[
            Property(
                key=prop.get("key"),
                value=prop.get("value"),
            ) for prop in item.get("properties")
        ]
    )


class SastResourceManagementServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_sast_scan_allocation_info(self, scan_id) -> SastScan:
        """

        Args:
            scan_id (str):

        Returns:
            SastScan
        """
        relative_url = api_url + "/scans/{id}".format(id=scan_id)
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_sast_scan(item)

    def delete_sast_scan(self, scan_id: str) -> bool:
        """

        Args:
            scan_id (str):

        Returns:
            bool
        """
        is_successful = False
        relative_url = api_url + "/scans/{id}".format(id=scan_id)
        response = self.api_client.delete_request(relative_url=relative_url)
        if response.status_code == NO_CONTENT:
            is_successful = True
        return is_successful

    def get_sast_scans(
            self, offset: int = 0, limit: int = 20, ids: List[str] = None, with_deleted: bool = None
    ) -> dict:
        """

        Args:
            offset (int): The number of items to skip before starting to collect the result set.
            limit (int): The number of items to return.
            ids (list of str): Ids of scans to return.
            with_deleted (bool): If deleted scans should be included in result.

        Returns:
            dict
        """
        type_check(offset, int)
        type_check(limit, int)
        type_check(ids, list)
        list_member_type_check(ids, str)
        type_check(with_deleted, bool)

        relative_url = api_url + "/scans"
        params = {"offset": offset, "limit": limit, "ids": ids, "with-deleted": with_deleted}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return {
            "totalCount": 0,
            "scans": [
                construct_sast_scan(scan) for scan in item.get("scans")
            ]
        }


def get_sast_scan_allocation_info(scan_id) -> SastScan:
    return SastResourceManagementServiceAPI().get_sast_scan_allocation_info(scan_id=scan_id)


def delete_sast_scan(scan_id: str) -> bool:
    return SastResourceManagementServiceAPI().delete_sast_scan(scan_id=scan_id)


def get_sast_scans(
        offset: int = 0, limit: int = 20, ids: List[str] = None, with_deleted: bool = None
) -> dict:
    return SastResourceManagementServiceAPI().get_sast_scans(
        offset=offset, limit=limit, ids=ids, with_deleted=with_deleted
    )
