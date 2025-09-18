from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import (
    ScanInfoCollection, construct_scan_info_collection,
    ScanInfo, construct_scan_info,
    EngineMetrics, construct_engine_metrics,
    ScanEngineVersion, construct_scan_engine_version,
)

api_url = "/api/sast-metadata"


class SastScanMetadataServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_metadata_of_scans(self, scan_ids: List[str]) -> ScanInfoCollection:
        """

        Args:
            scan_ids (list of str):

        Returns:
            ScanInfoCollection
        """
        type_check(scan_ids, list)
        list_member_type_check(scan_ids, str)
        relative_url = api_url
        params = {"scan-ids": scan_ids}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return construct_scan_info_collection(response)

    def get_metadata_of_scan(self, scan_id: str) -> ScanInfo:
        """

       Args:
           scan_id (str):

       Returns:
            ScanInfo
       """
        type_check(scan_id, str)
        relative_url = api_url + f"/{scan_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        response = response.json()
        return construct_scan_info(response)

    def get_engine_metrics_of_scan(self, scan_id: str) -> EngineMetrics:
        """

        Args:
            scan_id (str):

        Returns:
            EngineMetrics
        """
        type_check(scan_id, str)
        relative_url = api_url + f"/{scan_id}/metrics"
        response = self.api_client.get_request(relative_url=relative_url)
        response = response.json()
        return construct_engine_metrics(response)

    def get_engine_versions_of_scan(self, scan_ids: List[str]) -> List[ScanEngineVersion]:
        """

         Args:
             scan_ids (list of str):

         Returns:
             list of ScanEngineVersion
         """
        type_check(scan_ids, list)
        list_member_type_check(scan_ids, str)
        relative_url = api_url + "/engine-version"
        params = {"scan-ids": scan_ids}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return [
            construct_scan_engine_version(item) for item in response or []
        ]


def get_metadata_of_scans(scan_ids: List[str]) -> ScanInfoCollection:
    return SastScanMetadataServiceAPI().get_metadata_of_scans(scan_ids=scan_ids)


def get_metadata_of_scan(scan_id: str) -> ScanInfo:
    return SastScanMetadataServiceAPI().get_metadata_of_scan(scan_id=scan_id)


def get_engine_metrics_of_scan(scan_id: str) -> EngineMetrics:
    return SastScanMetadataServiceAPI().get_engine_metrics_of_scan(scan_id=scan_id)


def get_engine_versions_of_scan(scan_ids: List[str]) -> List[ScanEngineVersion]:
    return SastScanMetadataServiceAPI().get_engine_versions_of_scan(scan_ids=scan_ids)
