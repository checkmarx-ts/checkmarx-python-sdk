from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import (
    ScanInfoCollection,
    ScanInfo,
    EngineMetrics,
    ScanEngineVersion,
)

api_url = "/api/sast-metadata"


def construct_scan_info(scan_info):
    """

    Args:
        scan_info (dict):

    Returns:
        ScanInfo
    """
    return ScanInfo(
        scan_id=scan_info.get("scanId"),
        project_id=scan_info.get("projectId"),
        loc=scan_info.get("loc"),
        file_count=scan_info.get("fileCount"),
        is_incremental=scan_info.get("isIncremental"),
        is_incremental_canceled=scan_info.get("isIncrementalCanceled"),
        incremental_cancel_reason=scan_info.get("incrementalCancelReason"),
        based_id=scan_info.get("baseId"),
        added_files_count=scan_info.get("addedFilesCount"),
        changed_files_count=scan_info.get("changedFilesCount"),
        deleted_files_count=scan_info.get("deletedFilesCount"),
        change_percentage=scan_info.get("changePercentage"),
        query_preset=scan_info.get("queryPreset"),
    )


def construct_engine_metric(engine_metrics):
    """

    Args:
        engine_metrics (dict):

    Returns:
        EngineMetrics
    """
    return EngineMetrics(
        scan_id=engine_metrics.get("scanId"),
        memory_peak=engine_metrics.get("memoryPeak"),
        virtual_memory_peak=engine_metrics.get("virtualMemoryPeak"),
        total_scanned_files_count=engine_metrics.get("totalScannedFilesCount"),
        total_scanned_loc=engine_metrics.get("totalScannedLoc"),
        dom_objects_per_language=engine_metrics.get("domObjectsPerLanguage"),
        successful_loc_per_language=engine_metrics.get("successfullLocPerLanguage"),
        failed_loc_per_language=engine_metrics.get("failedLocPerLanguage"),
        file_count_of_detected_but_not_scanned_languages=engine_metrics.get(
            "fileCountOfDetectedButNotScannedLanguages"),
        scanned_files_per_language=engine_metrics.get("scannedFilesPerLanguage")
    )


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
        return ScanInfoCollection(
            total_count=response.get("totalCount"),
            scans=[
                construct_scan_info(scan_info) for scan_info in response.get("scans")
            ],
            missing=response.get("missing")
        )

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
        return construct_scan_info(scan_info=response)

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
        return construct_engine_metric(engine_metrics=response)

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
            ScanEngineVersion(
                scan_id=item.get("scanId"),
                project_id=item.get("projectId"),
                tenant_id=item.get("tenantId"),
                engine_version=item.get("engineVersion")
            ) for item in response
        ]


def get_metadata_of_scans(scan_ids: List[str]) -> ScanInfoCollection:
    return SastScanMetadataServiceAPI().get_metadata_of_scans(scan_ids=scan_ids)


def get_metadata_of_scan(scan_id: str) -> ScanInfo:
    return SastScanMetadataServiceAPI().get_metadata_of_scan(scan_id=scan_id)


def get_engine_metrics_of_scan(scan_id: str) -> EngineMetrics:
    return SastScanMetadataServiceAPI().get_engine_metrics_of_scan(scan_id=scan_id)


def get_engine_versions_of_scan(scan_ids: List[str]) -> List[ScanEngineVersion]:
    return SastScanMetadataServiceAPI().get_engine_versions_of_scan(scan_ids=scan_ids)
