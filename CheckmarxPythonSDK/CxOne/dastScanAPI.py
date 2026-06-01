"""DAST Scans Service REST API.

Endpoints under <server>/api/dast/scans. Endpoints with documented
response shapes return DTO objects; the rest are stubs that return
the raw parsed JSON response until their schemas are pinned down.
"""
import json
from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import TenantOverview, DastEnvironmentsCollection


class DastScanAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/dast/scans"
        )

    # ----- General -----

    def get_tenant_overview(self) -> TenantOverview:
        """GET /tenant — aggregated data about DAST Environments in the tenant.

        Returns:
            TenantOverview with tenant_id, environments_count, risk_rating.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/tenant"
        )
        return TenantOverview.from_dict(response.json())

    # ----- Environments -----

    def create_environment(self, environment: dict) -> dict:
        """POST /environment — create a new Environment to be scanned by DAST."""
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/environment", json=environment
        )
        return response.json()

    def update_environment(self, environment: dict) -> dict:
        """PUT /environment — update an existing DAST Environment."""
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/environment", json=environment
        )
        return response.json()

    def delete_environment(self, environment: dict) -> bool:
        """DELETE /environment — delete an existing DAST Environment."""
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/environment", json=environment
        )
        return 200 <= response.status_code < 300

    def get_environment_by_id(self, env_id: str) -> dict:
        """GET /environment/{envId} — retrieve a specific Environment."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environment/{env_id}"
        )
        return response.json()

    def get_environments(
        self,
        filter: dict = None,
        from_: int = None,
        groups: List[str] = None,
        last_status: List[str] = None,
        match: dict = None,
        search: str = None,
        sort: List[str] = None,
        tags: List[str] = None,
        to: int = None,
    ) -> DastEnvironmentsCollection:
        """GET /environments — DAST Environments with their most recent scan
        summary and risk overview.

        Args:
            filter (dict, optional): Partial match on domain, url, scantype,
                environmentId, projectId, lastRiskRating, authSuccess,
                tunnelState. Serialized to JSON in the query string.
            from_ (int, optional): Pagination start offset. Default 0.
            groups (list of str, optional): Filter by user groups.
            last_status (list of str, optional): Filter by last scan status —
                New, Running, Finished, Failed, Cancelled.
            match (dict, optional): Exact match on the same fields as filter.
            search (str, optional): Substring search in domain or url.
            sort (list of str, optional): Sort by domain, url, scantype,
                lastscantime, lastscanstatus, lastriskrating, created,
                authsuccess.
            tags (list of str, optional): Filter by tags.
            to (int, optional): Pagination end offset.

        Returns:
            DastEnvironmentsCollection
        """
        params = {
            "filter": json.dumps(filter) if filter is not None else None,
            "from": from_,
            "groups": groups,
            "lastStatus": last_status,
            "match": json.dumps(match) if match is not None else None,
            "search": search,
            "sort": sort,
            "tags": tags,
            "to": to,
        }
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments", params=params
        )
        return DastEnvironmentsCollection.from_dict(response.json())

    def get_environments_count_by_group(self, group_by: str = None, **params) -> dict:
        """GET /environments/groups — count Environments grouped by a parameter
        (e.g. domain, url)."""
        query = {"groupBy": group_by, **params}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments/groups", params=query
        )
        return response.json()

    # ----- Scans -----

    def get_scans(self, **params) -> dict:
        """GET /scans — DAST scans run in the account with a risks overview."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scans", params=params
        )
        return response.json()

    def run_scan(self, scan: dict) -> dict:
        """POST /scan — run a DAST scan on an Environment."""
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/scan", json=scan
        )
        return response.json()

    def update_scan(self, scan: dict) -> dict:
        """PUT /scan — edit the configuration of an existing scan."""
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/scan", json=scan
        )
        return response.json()

    def cancel_scan(self, scan: dict) -> bool:
        """PATCH /scan — cancel a scan that is currently running."""
        response = self.api_client.call_api(
            method="PATCH", url=f"{self.base_url}/scan", json=scan
        )
        return 200 <= response.status_code < 300

    def delete_scan(self, scan: dict) -> bool:
        """DELETE /scan — delete an existing scan."""
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/scan", json=scan
        )
        return 200 <= response.status_code < 300

    def get_scans_count_by_group(self, group_by: str = None, **params) -> dict:
        """GET /scans/groups — count scans grouped by a parameter (e.g.
        initiator, scantype)."""
        query = {"groupBy": group_by, **params}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scans/groups", params=query
        )
        return response.json()

    def get_scan_by_id(self, scan_id: str) -> dict:
        """GET /scan/{scanId} — info about a specific DAST scan with a
        risks overview."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scan/{scan_id}"
        )
        return response.json()

    def get_scan_log(self, scan_id: str) -> str:
        """GET /log/{scanId} — retrieve the log for a scan."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/log/{scan_id}"
        )
        return response.text


# ----- Module-level conveniences -----

def get_tenant_overview() -> TenantOverview:
    return DastScanAPI().get_tenant_overview()


def create_environment(environment: dict) -> dict:
    return DastScanAPI().create_environment(environment=environment)


def update_environment(environment: dict) -> dict:
    return DastScanAPI().update_environment(environment=environment)


def delete_environment(environment: dict) -> bool:
    return DastScanAPI().delete_environment(environment=environment)


def get_environment_by_id(env_id: str) -> dict:
    return DastScanAPI().get_environment_by_id(env_id=env_id)


def get_environments(
    filter: dict = None,
    from_: int = None,
    groups: List[str] = None,
    last_status: List[str] = None,
    match: dict = None,
    search: str = None,
    sort: List[str] = None,
    tags: List[str] = None,
    to: int = None,
) -> DastEnvironmentsCollection:
    return DastScanAPI().get_environments(
        filter=filter, from_=from_, groups=groups, last_status=last_status,
        match=match, search=search, sort=sort, tags=tags, to=to,
    )


def get_environments_count_by_group(group_by: str = None, **params) -> dict:
    return DastScanAPI().get_environments_count_by_group(group_by=group_by, **params)


def get_scans(**params) -> dict:
    return DastScanAPI().get_scans(**params)


def run_scan(scan: dict) -> dict:
    return DastScanAPI().run_scan(scan=scan)


def update_scan(scan: dict) -> dict:
    return DastScanAPI().update_scan(scan=scan)


def dast_cancel_scan(scan: dict) -> bool:
    return DastScanAPI().cancel_scan(scan=scan)


def dast_delete_scan(scan: dict) -> bool:
    return DastScanAPI().delete_scan(scan=scan)


def get_scans_count_by_group(group_by: str = None, **params) -> dict:
    return DastScanAPI().get_scans_count_by_group(group_by=group_by, **params)


def dast_get_scan_by_id(scan_id: str) -> dict:
    return DastScanAPI().get_scan_by_id(scan_id=scan_id)


def get_scan_log(scan_id: str) -> str:
    return DastScanAPI().get_scan_log(scan_id=scan_id)
