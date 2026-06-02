from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class DataRetentionAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/data-retention"
        )

    def get_data_retention_processes(
        self, offset: int = 0, limit: int = 25
    ) -> dict:
        """
        Get a data retention processes list.

        Args:
            offset (int): Items to skip. Default: 0
            limit (int): Max results (1-200). Default: 25

        Returns:
            dict with totalCount and configs
        """
        url = f"{self.base_url}"
        params = {"offset": offset, "limit": limit}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_locked_scans(
        self,
        date_from: str = None,
        date_to: str = None,
        offset: int = 0,
        limit: int = 25,
    ) -> dict:
        """
        Get the list of locked scans.

        Args:
            date_from (str): Earliest date (RFC3339)
            date_to (str): Latest date (RFC3339)
            offset (int): Items to skip. Default: 0
            limit (int): Max results (1-200). Default: 25

        Returns:
            dict with totalCount, filteredCount, lockedScans
        """
        url = f"{self.base_url}/scans/locked"
        params = {
            "date_from": date_from,
            "date_to": date_to,
            "offset": offset,
            "limit": limit,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_process_status(
        self, id: str, offset: int = 0, limit: int = 25
    ) -> dict:
        """
        Get the status of a data retention process.

        Args:
            id (str): The data retention config ID (uuid)
            offset (int): Items to skip. Default: 0
            limit (int): Max results (1-200). Default: 25

        Returns:
            dict with id, status, statusDetails, totalDetailsCount, details
        """
        url = f"{self.base_url}/{id}/status"
        params = {"offset": offset, "limit": limit}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def lock_scans(self, scan_ids: List[str]) -> dict:
        """
        Lock specific scans to prevent deletion during data retention.

        Args:
            scan_ids (List[str]): Scan IDs to lock (1-100 UUIDs)

        Returns:
            dict with message, lockedScans, failedAttempts
        """
        url = f"{self.base_url}/scans/lock"
        body = {"scanIds": scan_ids}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def unlock_scans(self, scan_ids: List[str]) -> dict:
        """
        Unlock previously locked scans.

        Args:
            scan_ids (List[str]): Scan IDs to unlock (1-100 UUIDs)

        Returns:
            dict with message, unlockedScans, failedAttempts
        """
        url = f"{self.base_url}/scans/unlock"
        body = {"scanIds": scan_ids}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def start_data_retention_process(
        self,
        from_date: str = None,
        to_date: str = None,
        scans_to_keep: int = None,
    ) -> dict:
        """
        Start a data retention process for the tenant.

        Provide either (from_date + to_date) OR scans_to_keep.

        Args:
            from_date (str): Start date (RFC3339)
            to_date (str): End date (RFC3339)
            scans_to_keep (int): Number of successful scans to keep per project

        Returns:
            dict with id (the data retention config ID)
        """
        url = f"{self.base_url}/tenant"
        if scans_to_keep is not None:
            body = {"scansToKeep": scans_to_keep}
        else:
            body = {"fromDate": from_date, "toDate": to_date}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def abort_process(self, id: str) -> bool:
        """
        Abort a data retention process.

        Args:
            id (str): The data retention config ID (uuid)

        Returns:
            bool
        """
        url = f"{self.base_url}/{id}/abort"
        response = self.api_client.call_api(method="POST", url=url)
        return response.status_code == 200


# ---- Module-level convenience functions ----

def get_data_retention_processes(
    offset: int = 0, limit: int = 25
) -> dict:
    return DataRetentionAPI().get_data_retention_processes(
        offset=offset, limit=limit
    )


def get_locked_scans(
    date_from: str = None,
    date_to: str = None,
    offset: int = 0,
    limit: int = 25,
) -> dict:
    return DataRetentionAPI().get_locked_scans(
        date_from=date_from, date_to=date_to, offset=offset, limit=limit
    )


def get_process_status(
    id: str, offset: int = 0, limit: int = 25
) -> dict:
    return DataRetentionAPI().get_process_status(
        id=id, offset=offset, limit=limit
    )


def lock_scans(scan_ids: List[str]) -> dict:
    return DataRetentionAPI().lock_scans(scan_ids=scan_ids)


def unlock_scans(scan_ids: List[str]) -> dict:
    return DataRetentionAPI().unlock_scans(scan_ids=scan_ids)


def start_data_retention_process(
    from_date: str = None,
    to_date: str = None,
    scans_to_keep: int = None,
) -> dict:
    return DataRetentionAPI().start_data_retention_process(
        from_date=from_date, to_date=to_date, scans_to_keep=scans_to_keep
    )


def abort_process(id: str) -> bool:
    return DataRetentionAPI().abort_process(id=id)
