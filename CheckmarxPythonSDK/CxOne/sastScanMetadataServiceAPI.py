from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    ScanInfoCollection,
    ScanInfo,
    EngineMetrics,
    ScanEngineVersion,
)


class SastScanMetadataServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/sast-metadata"
        )

    def get_metadata_of_scans(
        self, scan_ids: List[str]
    ) -> ScanInfoCollection:
        """
        Args:
            scan_ids (list of str):

        Returns:
            ScanInfoCollection
        """
        params = {"scan-ids": scan_ids}
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return ScanInfoCollection.from_dict(response.json())

    def get_metadata_of_scan(self, scan_id: str) -> ScanInfo:
        """
        Args:
            scan_id (str):

        Returns:
            ScanInfo
        """
        url = f"{self.base_url}/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return ScanInfo.from_dict(response.json())

    def get_engine_metrics_of_scan(self, scan_id: str) -> EngineMetrics:
        """
        Args:
            scan_id (str):

        Returns:
            EngineMetrics
        """
        url = f"{self.base_url}/{scan_id}/metrics"
        response = self.api_client.call_api(method="GET", url=url)
        return EngineMetrics.from_dict(response.json())

    def get_engine_versions_of_scan(
        self, scan_ids: List[str]
    ) -> List[ScanEngineVersion]:
        """
        Args:
            scan_ids (list of str):

        Returns:
            list of ScanEngineVersion
        """
        url = f"{self.base_url}/engine-version"
        params = {"scan-ids": scan_ids}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [
            ScanEngineVersion.from_dict(item)
            for item in (response.json() or [])
        ]


def get_metadata_of_scans(scan_ids: List[str]) -> ScanInfoCollection:
    return SastScanMetadataServiceAPI().get_metadata_of_scans(
        scan_ids=scan_ids
    )


def get_metadata_of_scan(scan_id: str) -> ScanInfo:
    return SastScanMetadataServiceAPI().get_metadata_of_scan(
        scan_id=scan_id
    )


def get_engine_metrics_of_scan(scan_id: str) -> EngineMetrics:
    return SastScanMetadataServiceAPI().get_engine_metrics_of_scan(
        scan_id=scan_id
    )


def get_engine_versions_of_scan(
    scan_ids: List[str],
) -> List[ScanEngineVersion]:
    return SastScanMetadataServiceAPI().get_engine_versions_of_scan(
        scan_ids=scan_ids
    )
