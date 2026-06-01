from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, OK
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

    def delete_persisted_dom(
        self, project_id: str, scan_id: str, branch: str = None
    ) -> bool:
        """
        Delete the persisted DOM for a scan.

        Args:
            project_id (str):
            scan_id (str):
            branch (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/delete-persisted-dom"
        params = {"project-id": project_id, "scan-id": scan_id, "branch": branch}
        response = self.api_client.call_api(
            method="DELETE", url=url, params=params
        )
        return response.status_code == NO_CONTENT

    def get_default_file_exclusion_config(self) -> dict:
        """
        Get the default file exclusion config.

        Returns:
            dict
        """
        url = f"{self.base_url}/default-file-exclusion-config"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_tenant_file_exclusion_config(self) -> dict:
        """
        Get the tenant file exclusion config.

        Returns:
            dict
        """
        url = f"{self.base_url}/file-exclusion-config"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_project_file_exclusion_config(self, project_id: str) -> dict:
        """
        Get the project file exclusion config.

        Args:
            project_id (str):

        Returns:
            dict
        """
        url = f"{self.base_url}/{project_id}/file-exclusion-config"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def check_persisted_dom_exists(
        self, project_id: str, scan_id: str, branch: str = None
    ) -> bool:
        """
        Check whether the persisted DOM exists for a scan.

        Args:
            project_id (str):
            scan_id (str):
            branch (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/exists-persisted-dom"
        params = {"project-id": project_id, "scan-id": scan_id, "branch": branch}
        response = self.api_client.call_api(
            method="HEAD", url=url, params=params
        )
        return response.status_code == OK

    def update_tenant_file_exclusion_config(self, config: dict) -> dict:
        """
        Update the tenant file exclusion config.

        Args:
            config (dict): Key-value pairs mapping exclusion rule names
                to boolean values.

        Returns:
            dict
        """
        url = f"{self.base_url}/file-exclusion-config"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=config
        )
        return response.json()

    def update_project_file_exclusion_config(
        self, project_id: str, config: dict
    ) -> dict:
        """
        Update the project file exclusion config.

        Args:
            project_id (str):
            config (dict): Key-value pairs mapping exclusion rule names
                to boolean values.

        Returns:
            dict
        """
        url = f"{self.base_url}/{project_id}/file-exclusion-config"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=config
        )
        return response.json()


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


def delete_persisted_dom(
    project_id: str, scan_id: str, branch: str = None
) -> bool:
    return SastScanMetadataServiceAPI().delete_persisted_dom(
        project_id=project_id, scan_id=scan_id, branch=branch
    )


def get_default_file_exclusion_config() -> dict:
    return SastScanMetadataServiceAPI().get_default_file_exclusion_config()


def get_tenant_file_exclusion_config() -> dict:
    return SastScanMetadataServiceAPI().get_tenant_file_exclusion_config()


def get_project_file_exclusion_config(project_id: str) -> dict:
    return SastScanMetadataServiceAPI().get_project_file_exclusion_config(
        project_id=project_id
    )


def check_persisted_dom_exists(
    project_id: str, scan_id: str, branch: str = None
) -> bool:
    return SastScanMetadataServiceAPI().check_persisted_dom_exists(
        project_id=project_id, scan_id=scan_id, branch=branch
    )


def update_tenant_file_exclusion_config(config: dict) -> dict:
    return SastScanMetadataServiceAPI().update_tenant_file_exclusion_config(
        config=config
    )


def update_project_file_exclusion_config(
    project_id: str, config: dict
) -> dict:
    return SastScanMetadataServiceAPI().update_project_file_exclusion_config(
        project_id=project_id, config=config
    )
