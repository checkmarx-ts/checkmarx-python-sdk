"""DAST Scans Service REST API.

Endpoints under <server>/api/dast/scans. Endpoints with documented
response shapes return DTO objects; the rest are stubs that return
the raw parsed JSON response until their schemas are pinned down.
"""
import os
from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    TenantOverview,
    DastEnvironment,
    DastEnvironmentsCollection,
    DastEnvironmentFilter,
    DastEnvironmentGroupCount,
    DastEnvironmentInput,
    DastEnvironmentUpdate,
    DastGroupBy,
    DastRunScanInput,
    DastScanType,
    DastScanUpdate,
    DastSortBy,
)


def _flatten_object_param(name: str, obj_filter) -> dict:
    """Expand a DastEnvironmentFilter into bracketed nested query params
    (e.g. filter[scantype]=DAST), which is what the API expects."""
    if obj_filter is None:
        return {}
    return {f"{name}[{k}]": v for k, v in obj_filter.to_dict().items()}


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

    def create_environment(self, environment: DastEnvironmentInput) -> str:
        """POST /environment — create a new Environment to be scanned by DAST.

        Args:
            environment (DastEnvironmentInput): the new Environment's
                configuration. domain, url, and scan_type are required.

        Returns:
            str: the unique identifier of the created Environment in
            Checkmarx One. The endpoint responds with plain text
            (Accept: text/plain).
        """
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/environment",
            json=environment.to_dict(),
        )
        env_id = response.text.strip()
        # The endpoint returns the raw UUID, but some gateways wrap it in
        # quotes — strip them so callers always get a bare id.
        if env_id.startswith('"') and env_id.endswith('"'):
            env_id = env_id[1:-1]
        return env_id

    def update_environment(self, environment: DastEnvironmentUpdate) -> bool:
        """PUT /environment — update an existing DAST Environment.

        Args:
            environment (DastEnvironmentUpdate): the partial update.
                environment_id is required; only the fields you set are
                sent (None values are dropped).

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/environment",
            json=environment.to_dict(),
        )
        return 200 <= response.status_code < 300

    def delete_environment(self, environment_id: str) -> bool:
        """DELETE /environment — delete an existing DAST Environment.

        Args:
            environment_id (str): UUID of the Environment to delete.
                Passed as the `environmentId` query parameter.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/environment",
            params={"environmentId": environment_id},
        )
        return 200 <= response.status_code < 300

    def get_environment_by_id(self, env_id: str) -> DastEnvironment:
        """GET /environment/{envId} — retrieve a specific Environment by
        UUID, including its most recent scan summary and risk overview.

        Args:
            env_id (str): the Environment's UUID.

        Returns:
            DastEnvironment
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environment/{env_id}"
        )
        return DastEnvironment.from_dict(response.json())

    def get_environments(
        self,
        filter_: DastEnvironmentFilter = None,
        from_: int = None,
        groups: List[str] = None,
        last_status: List[str] = None,
        match: DastEnvironmentFilter = None,
        search: str = None,
        sort: List[DastSortBy] = None,
        tags: List[str] = None,
        to: int = None,
    ) -> DastEnvironmentsCollection:
        """GET /environments — DAST Environments with their most recent scan
        summary and risk overview.

        Args:
            filter_ (DastEnvironmentFilter, optional): Partial-match filter on
                domain, url, scan_type, environment_id, project_id,
                last_risk_rating, auth_success, tunnel_state. Serialized to
                JSON in the query string. (Trailing underscore avoids
                shadowing the built-in `filter`.)
            from_ (int, optional): Pagination start offset. Default 0.
            groups (list of str, optional): Filter by user groups.
            last_status (list of str, optional): Filter by last scan status —
                New, Running, Finished, Failed, Cancelled.
            match (DastEnvironmentFilter, optional): Exact-match filter on the
                same fields as `filter`.
            search (str, optional): Substring search in domain or url.
            sort (list of DastSortBy, optional): Columns to sort by, in
                priority order. Each entry is serialized as "<column>:asc";
                pass a raw "<column>:desc" string in the list to override
                direction per column. The live API rejects bare column
                names with HTTP 400 even though the published spec lists
                only column names. Valid columns are domain, url, scantype,
                lastscantime, lastscanstatus, lastriskrating, created,
                authsuccess.
            tags (list of str, optional): Filter by tags.
            to (int, optional): Pagination end offset.

        Returns:
            DastEnvironmentsCollection
        """
        params = {
            "from": from_,
            "groups": groups,
            "lastStatus": last_status,
            "search": search,
            # Default direction is asc; caller can pass a raw "col:desc"
            # string in the list to override per column.
            "sort": (
                [s if ":" in str(s) else f"{s.value if isinstance(s, DastSortBy) else s}:asc"
                 for s in sort]
                if sort else None
            ),
            "tags": tags,
            "to": to,
        }
        params.update(_flatten_object_param("filter", filter_))
        params.update(_flatten_object_param("match", match))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments", params=params
        )
        return DastEnvironmentsCollection.from_dict(response.json())

    def get_environments_count_by_group(
        self,
        group_by: List[DastGroupBy],
        filter_: DastEnvironmentFilter = None,
        groups: List[str] = None,
        search: str = None,
        tags: List[str] = None,
    ) -> List[DastEnvironmentGroupCount]:
        """GET /environments/groups — count of Environments per group.

        Args:
            group_by (list of DastGroupBy): one or more columns to group by.
                Required.
            filter_ (DastEnvironmentFilter, optional): partial-match filter.
                (Trailing underscore avoids shadowing the built-in `filter`.)
            groups (list of str, optional): filter by user groups.
            search (str, optional): substring search in domain or url.
            tags (list of str, optional): filter by tags.

        Returns:
            list of DastEnvironmentGroupCount, one per bucket.
        """
        params = {
            "groupBy": [g.value if isinstance(g, DastGroupBy) else g for g in group_by],
            "groups": groups,
            "search": search,
            "tags": tags,
        }
        params.update(_flatten_object_param("filter", filter_))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments/groups", params=params,
        )
        return [DastEnvironmentGroupCount.from_dict(b) for b in (response.json() or [])]

    # ----- Scans -----

    def get_scans(self, **params) -> dict:
        """GET /scans — DAST scans run in the account with a risks overview."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scans", params=params
        )
        return response.json()

    def run_scan(self, scan: DastRunScanInput) -> str:
        """POST /scan — run a DAST scan on an Environment via multipart upload.

        Args:
            scan (DastRunScanInput): environment_id, scan_type, and
                configuration_file (local path to the ZAP config) are
                required. api_file (path to an OpenAPI/Swagger file)
                is optional.

        Returns:
            str: the unique identifier of the created scan. The endpoint
            responds with plain text (text/plain).
        """
        # Build form-field data; httpx serializes lists as repeated parts.
        # Booleans are sent as lowercase "true"/"false" — the JSON-spec form
        # that DAST backends generally accept.
        def _bool(v):
            return None if v is None else ("true" if v else "false")

        data = {
            "environmentID": scan.environment_id,
            "scanType": (
                scan.scan_type.value if isinstance(scan.scan_type, DastScanType)
                else scan.scan_type
            ),
            "groups": scan.groups,
            "tags": scan.tags,
            "useExternalWorker": _bool(scan.use_external_worker),
            "useAuthSession": _bool(scan.use_auth_session),
            "apiFileType": scan.api_file_type,
            "cliVersion": scan.cli_version,
            "heartbeatInterval": scan.heartbeat_interval,
        }
        data = {k: v for k, v in data.items() if v is not None}

        # Open files for the request. httpx closes the stream on its own.
        files = {}
        if scan.configuration_file:
            files["configurationFile"] = (
                os.path.basename(scan.configuration_file),
                open(scan.configuration_file, "rb"),
                "application/octet-stream",
            )
        if scan.api_file:
            files["APIFile"] = (
                os.path.basename(scan.api_file),
                open(scan.api_file, "rb"),
                "application/octet-stream",
            )

        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/scan",
            data=data, files=files,
        )
        scan_id = response.text.strip()
        if scan_id.startswith('"') and scan_id.endswith('"'):
            scan_id = scan_id[1:-1]
        return scan_id

    def update_scan(self, scan: DastScanUpdate) -> str:
        """PUT /scan — edit the configuration of an existing scan.

        Args:
            scan (DastScanUpdate): the partial update. scan_id and
                environment_id are required; only set fields are sent.

        Returns:
            str: the API's plain-text response body (typically empty or
            the scan id on success).
        """
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/scan",
            json=scan.to_dict(),
        )
        body = response.text.strip()
        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]
        return body

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


def create_environment(environment: DastEnvironmentInput) -> str:
    return DastScanAPI().create_environment(environment=environment)


def update_environment(environment: DastEnvironmentUpdate) -> bool:
    return DastScanAPI().update_environment(environment=environment)


def delete_environment(environment_id: str) -> bool:
    return DastScanAPI().delete_environment(environment_id=environment_id)


def get_environment_by_id(env_id: str) -> DastEnvironment:
    return DastScanAPI().get_environment_by_id(env_id=env_id)


def get_environments(
    filter_: DastEnvironmentFilter = None,
    from_: int = None,
    groups: List[str] = None,
    last_status: List[str] = None,
    match: DastEnvironmentFilter = None,
    search: str = None,
    sort: List[DastSortBy] = None,
    tags: List[str] = None,
    to: int = None,
) -> DastEnvironmentsCollection:
    return DastScanAPI().get_environments(
        filter_=filter_, from_=from_, groups=groups, last_status=last_status,
        match=match, search=search, sort=sort, tags=tags, to=to,
    )


def get_environments_count_by_group(
    group_by: List[DastGroupBy],
    filter_: DastEnvironmentFilter = None,
    groups: List[str] = None,
    search: str = None,
    tags: List[str] = None,
) -> List[DastEnvironmentGroupCount]:
    return DastScanAPI().get_environments_count_by_group(
        group_by=group_by, filter_=filter_, groups=groups, search=search, tags=tags,
    )


def get_scans(**params) -> dict:
    return DastScanAPI().get_scans(**params)


def run_scan(scan: DastRunScanInput) -> str:
    return DastScanAPI().run_scan(scan=scan)


def update_scan(scan: DastScanUpdate) -> str:
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
