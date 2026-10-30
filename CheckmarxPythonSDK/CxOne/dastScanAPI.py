"""DAST Scans Service REST API.

Endpoints under <server>/api/dast/scans. Endpoints with documented
response shapes return DTO objects; the rest are stubs that return
the raw parsed JSON response until their schemas are pinned down.
"""
import json
import os
from typing import Dict, List, Optional
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    TenantOverview,
    DastApiFileWithType,
    DastApplicationEnvironmentInfo,
    DastApplicationEnvironmentWithPrimary,
    DastAuthSession,
    DastAuthSessionReportData,
    DastAuthSessionTotp,
    DastEnvironment,
    DastEnvironmentsCollection,
    DastEnvironmentFilter,
    DastEnvironmentGroupCount,
    DastEnvironmentInput,
    DastEnvironmentUpdate,
    DastGroupBy,
    DastCorrelationCapacityResponse,
    DastCorrelationScansCollection,
    DastCreateTunnelResponse,
    DastFlagEnabled,
    DastPentestMaxProfile,
    DastPentestScansCollection,
    DastPentestScanSettings,
    DastRecording,
    DastRecordingWithPosition,
    DastRecordingsCollection,
    DastRunScanInput,
    DastScan,
    DastScanFilter,
    DastScanGroupBy,
    DastScanGroupCount,
    DastScanGroupFilter,
    DastScanSortBy,
    DastScanStatus,
    DastSequence,
    DastSequenceScriptsResponse,
    DastSimilarityIds,
    DastSequenceWithRecordingCount,
    DastTunnelResponse,
    DastTunnelsResponse,
    DastScanType,
    DastScanUpdate,
    DastScansCollection,
    DastSortBy,
    DastTotpField,
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

    def get_scans(
        self,
        environment_id: str,
        filter_: DastScanFilter = None,
        from_: int = None,
        groups: List[str] = None,
        last_status: List[DastScanStatus] = None,
        match: DastScanFilter = None,
        search: str = None,
        sort: List[DastScanSortBy] = None,
        tags: List[str] = None,
        to: int = None,
    ) -> DastScansCollection:
        """GET /scans — list scans for an Environment with a risks overview.

        Args:
            environment_id (str): UUID of the Environment. Required.
            filter_ (DastScanFilter, optional): partial-match filter on
                initiator, scan_type, project_id.
            from_ (int, optional): pagination start offset.
            groups (list of str, optional): filter by user groups.
            last_status (list of DastScanStatus, optional): filter by
                most recent scan status. Documented values are New,
                ExternalScan, Running, Finished, Failed, Cancelled.
            match (DastScanFilter, optional): exact-match filter.
            search (str, optional): substring search in initiator or
                lastStatus.
            sort (list of DastScanSortBy, optional): sort columns. Each
                entry is serialized as "<col>:asc"; pass a raw "col:desc"
                string in the list for per-column descending order.
            tags (list of str, optional): filter by tags.
            to (int, optional): pagination end offset.

        Returns:
            DastScansCollection
        """
        params = {
            "environmentId": environment_id,
            "from": from_,
            "groups": groups,
            "lastStatus": [
                s.value if isinstance(s, DastScanStatus) else s for s in last_status
            ] if last_status else None,
            "search": search,
            "sort": (
                [s if ":" in str(s) else f"{s.value if isinstance(s, DastScanSortBy) else s}:asc"
                 for s in sort]
                if sort else None
            ),
            "tags": tags,
            "to": to,
        }
        params.update(_flatten_object_param("filter", filter_))
        params.update(_flatten_object_param("match", match))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scans", params=params,
        )
        return DastScansCollection.from_dict(response.json())

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

        # Read files fully and pass bytes to httpx: file objects passed to
        # httpx are not closed by it, which leaks the handle and prevents
        # deleting the file afterwards on Windows.
        files = {}
        if scan.configuration_file:
            with open(scan.configuration_file, "rb") as fh:
                config_content = fh.read()
            files["configurationFile"] = (
                os.path.basename(scan.configuration_file),
                config_content,
                "application/octet-stream",
            )
        if scan.api_file:
            with open(scan.api_file, "rb") as fh:
                api_content = fh.read()
            files["APIFile"] = (
                os.path.basename(scan.api_file),
                api_content,
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

    def run_public_scan(self, environment_id: str) -> str:
        """POST /publicScan — start a scan against a preconfigured Environment.

        Unlike run_scan, no ZAP configuration file is uploaded; the
        Environment must already be set up via the Checkmarx One web UI
        (Workspaces > Environments > DAST Environment Setup Wizard).

        Args:
            environment_id (str): UUID of the preconfigured Environment.

        Returns:
            str: the UUID of the created scan, returned as plain text.
        """
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/publicScan",
            json={"environmentID": environment_id},
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

    def cancel_scan(self, scan_id: str, environment_id: str) -> bool:
        """PATCH /scan — cancel a scan that is currently running.

        Args:
            scan_id (str): UUID of the scan to cancel.
            environment_id (str): UUID of the Environment the scan
                is running on. Both are required by the API.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="PATCH", url=f"{self.base_url}/scan",
            json={"scanId": scan_id, "environmentID": environment_id},
        )
        return 200 <= response.status_code < 300

    def delete_scan(self, scan_id: str, environment_id: str) -> bool:
        """DELETE /scan — delete an existing DAST scan.

        Args:
            scan_id (str): UUID of the scan to delete.
            environment_id (str): UUID of the Environment the scan belongs
                to. Both are required and sent as query parameters.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/scan",
            params={"scanId": scan_id, "environmentId": environment_id},
        )
        return 200 <= response.status_code < 300

    def get_scans_count_by_group(
        self,
        environment_id: str,
        group_by: List[DastScanGroupBy] = None,
        filter_: DastScanGroupFilter = None,
        groups: List[str] = None,
        last_scan_status: List[DastScanStatus] = None,
        search: str = None,
        tags: List[str] = None,
    ) -> List[DastScanGroupCount]:
        """GET /scans/groups — count of scans per group on an Environment.

        Args:
            environment_id (str): UUID of the Environment. Required by
                the API. Sent as the `environmentID` query param
                (uppercase ID per the doc).
            group_by (list of DastScanGroupBy, optional): columns to
                group by. Documented values are initiator, scantype,
                projectId, riskRating.
            filter_ (DastScanGroupFilter, optional): partial-match filter
                on initiator, scan_type, risk_rating.
            groups (list of str, optional): filter by user groups.
            last_scan_status (list of DastScanStatus, optional): filter
                by last scan status. Sent as `LastScanStatus` (capital L).
            search (str, optional): substring search in initiator/lastStatus.
            tags (list of str, optional): filter by tags.

        Returns:
            list of DastScanGroupCount.
        """
        params = {
            "environmentID": environment_id,
            "groupBy": (
                [g.value if isinstance(g, DastScanGroupBy) else g for g in group_by]
                if group_by else None
            ),
            "groups": groups,
            "LastScanStatus": (
                [s.value if isinstance(s, DastScanStatus) else s for s in last_scan_status]
                if last_scan_status else None
            ),
            "search": search,
            "tags": tags,
        }
        params.update(_flatten_object_param("filter", filter_))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scans/groups", params=params,
        )
        return [DastScanGroupCount.from_dict(b) for b in (response.json() or [])]

    def get_scan_by_id(self, scan_id: str) -> DastScan:
        """GET /scan/{scanId} — info about a specific DAST scan including
        a risks overview.

        The live response shape is identical to one element of the
        get_scans response, so this reuses the existing DastScan DTO.
        (Doc claims riskLevel is a string and alertRiskLevel has short
        keys — both incorrect; live data has full object shape with
        criticalCount/highCount/etc.)

        Args:
            scan_id (str): UUID of the scan.

        Returns:
            DastScan
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/scan/{scan_id}"
        )
        return DastScan.from_dict(response.json())

    def get_scan_log(self, scan_id: str) -> bytes:
        """GET /log/{scanId} — download the log archive for a scan.

        Despite the doc's "text file" wording, the response is a binary
        ZIP archive (Content-Type: application/zip) containing the
        scan logs. The caller is responsible for writing it to disk
        if persistence is needed.

        Args:
            scan_id (str): UUID of the scan.

        Returns:
            bytes: raw ZIP file content.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/log/{scan_id}"
        )
        return response.content

    # ----- Auth Session -----
    #
    # A distinct sub-workflow from the `authSettings`/`scanConfig` nested on
    # DastEnvironment: these endpoints drive the interactive auth-session
    # setup/verification flow (browser-recorded login, config file upload,
    # credentials + TOTP, etc.) that happens before a scan can authenticate.

    def create_auth_session(
        self,
        environment_id: str,
        session_type: str,
        url: str,
        uuid: str = None,
        method: str = None,
    ) -> bool:
        """POST /authSession — create a new auth session for an Environment.

        Args:
            environment_id (str): UUID of the Environment. Required.
            session_type (str): The type of session being created.
                Required. Not documented/enumerated in the spec; "CLI" is
                confirmed to work live (other values tried — BROWSER,
                MANUAL, DAST, AUTH, and their lowercase forms — were
                rejected with a generic "validation failed" 400).
            url (str): The URL to authenticate against. Required.
            uuid (str, optional): UUID to use for the new session; the
                server generates one if omitted.
            method (str, optional): Auth method hint.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        body = {
            "EnvironmentID": environment_id,
            "SessionType": session_type,
            "URL": url,
            "UUID": uuid,
            "Method": method,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/authSession", json=body
        )
        return 200 <= response.status_code < 300

    def update_auth_session_api_file(
        self,
        uuid: str,
        environment_id: str,
        api_file: str,
        api_type: str = None,
        api_url: str = None,
        api_variables: Dict[str, str] = None,
    ) -> str:
        """PUT /authSession/apiFile — update the auth session's API
        definition file.

        Confirmed live: calling this on a session straight off
        create_auth_session (before any other PUT has committed a method
        on it, e.g. set_auth_session_no_auth or
        update_auth_session_credentials) returns 200 with a file id, but
        the file never actually attaches — get_auth_session_api_files_data
        comes back empty afterward. Settle the session's method first.

        Args:
            uuid (str): The auth session's UUID. Required.
            environment_id (str): UUID of the Environment. Required.
            api_file (str): Local path to the API definition file
                (OpenAPI/Postman/HAR/SOAP/GraphQL). Required.
            api_type (str, optional): OPENAPI, POSTMAN, HAR, SOAP, or
                GRAPHQL.
            api_url (str, optional): The API's base URL.
            api_variables (Dict[str, str], optional): Variable
                substitutions for the file; sent as a JSON-encoded string.

        Returns:
            str: the uploaded file's ID.
        """
        data = {
            "UUID": uuid,
            "EnvironmentID": environment_id,
            "APIType": api_type,
            "APIURL": api_url,
            "APIVariables": json.dumps(api_variables) if api_variables else None,
        }
        data = {k: v for k, v in data.items() if v is not None}
        with open(api_file, "rb") as fh:
            content = fh.read()
        files = {
            "APIFile": (os.path.basename(api_file), content, "application/octet-stream")
        }
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/apiFile",
            data=data, files=files,
        )
        return response.json().get("id")

    def validate_auth_session_api_file(
        self, api_file: str, api_type: str = None
    ) -> dict:
        """POST /authSession/apiFile/validate — validate an API definition
        file's extension and content before uploading it for real.

        Args:
            api_file (str): Local path to the API definition file. Required.
            api_type (str, optional): OPENAPI, POSTMAN, HAR, SOAP, or
                GRAPHQL.

        Returns:
            dict: {"valid": bool, "error": str}. Always returns 200 with
            the outcome in the body, even when invalid.
        """
        data = {"APIType": api_type} if api_type else {}
        with open(api_file, "rb") as fh:
            content = fh.read()
        files = {
            "APIFile": (os.path.basename(api_file), content, "application/octet-stream")
        }
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/authSession/apiFile/validate",
            data=data, files=files,
        )
        return response.json()

    def bulk_replace_auth_session_api_files(
        self,
        environment_id: str,
        auth_session_uuid: str = None,
        files: List[str] = None,
        api_types: List[str] = None,
        api_variables: List[Dict[str, str]] = None,
        api_urls: List[str] = None,
        file_ids_to_keep: List[str] = None,
        kept_files_updates: Dict[str, dict] = None,
    ) -> List[str]:
        """PUT /authSession/apiFiles — bulk replace the auth session's API
        definition files.

        This endpoint doesn't need an explicit auth session at all —
        passing only `environment_id` works, and it creates/updates the
        environment's auth session as a side effect. If you've just
        called create_auth_session yourself, see
        update_auth_session_api_file's docstring for a quirk around
        files not attaching until the session's method has settled.

        Args:
            environment_id (str): UUID of the Environment. Required.
            auth_session_uuid (str, optional): The auth session's UUID.
            files (List[str], optional): Local paths of new API definition
                files to upload.
            api_types (List[str], optional): One entry per `files` entry,
                in the same order. Must be the same length as `files`.
            api_variables (List[Dict[str, str]], optional): One entry per
                `files` entry; may be shorter than `files` (sparse). Each
                dict is sent JSON-encoded.
            api_urls (List[str], optional): One entry per `files` entry;
                may be shorter than `files` (sparse).
            file_ids_to_keep (List[str], optional): IDs of previously
                uploaded files to keep as-is.
            kept_files_updates (Dict[str, dict], optional): Updates
                ({apiVariables, apiUrl}) for kept files, keyed by file ID;
                sent as a single JSON-encoded object.

        Returns:
            List[str]: IDs of all files now associated with the auth
            session (kept + newly uploaded).
        """
        # httpx's multipart encoder takes repeated form fields as a list
        # *value* in the data dict (unlike `files`, which takes a list of
        # (name, file) tuples for repeats under the same field name).
        data: Dict[str, object] = {"environmentId": environment_id}
        if auth_session_uuid:
            data["AuthSessionUUID"] = auth_session_uuid
        if api_types:
            data["apiTypes"] = api_types
        if api_variables:
            data["apiVariables"] = [json.dumps(v) for v in api_variables]
        if api_urls:
            data["apiUrls"] = api_urls
        if file_ids_to_keep:
            data["fileIDsToKeep"] = file_ids_to_keep
        if kept_files_updates:
            data["keptFilesUpdates"] = json.dumps(kept_files_updates)

        file_fields = []
        for path in (files or []):
            with open(path, "rb") as fh:
                content = fh.read()
            file_fields.append(
                ("files", (os.path.basename(path), content, "application/octet-stream"))
            )

        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/apiFiles",
            data=data, files=file_fields,
        )
        return response.json().get("fileIDs", [])

    def update_auth_session_credentials(
        self,
        uuid: str,
        environment_id: str,
        login_page_url: str,
        user_name: str,
        password: str = None,
        use_existing_password: bool = None,
        totp: DastAuthSessionTotp = None,
        use_existing_totp_secret: bool = None,
        local_auth_test: bool = None,
        totp_field: DastTotpField = None,
    ) -> bool:
        """PUT /authSession/credentials — update the auth session's
        username/password credentials.

        Args:
            uuid (str): The auth session's UUID. Required.
            environment_id (str): UUID of the Environment. Required.
            login_page_url (str): The login page's URL. Required.
            user_name (str): The username to authenticate with. Required.
            password (str, optional): The password. Omit (with
                use_existing_password=True) to keep the stored password.
            use_existing_password (bool, optional): Keep the previously
                stored password.
            totp (DastAuthSessionTotp, optional): TOTP secret settings.
            use_existing_totp_secret (bool, optional): Keep the previously
                stored TOTP secret.
            local_auth_test (bool, optional): Whether to run the auth test
                from the local (non-tunneled) network.
            totp_field (DastTotpField, optional): The form field the TOTP
                code should be entered into.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        body = {
            "UUID": uuid,
            "EnvironmentID": environment_id,
            "LoginPageURL": login_page_url,
            "UserName": user_name,
            "Password": password,
            "UseExistingPassword": use_existing_password,
            "TOTP": totp.to_dict() if totp else None,
            "UseExistingTOTPSecret": use_existing_totp_secret,
            "LocalAuthTest": local_auth_test,
            "TotpField": totp_field.to_dict() if totp_field else None,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/credentials", json=body,
        )
        return 200 <= response.status_code < 300

    def update_auth_session_file(
        self,
        uuid: str,
        environment_id: str,
        method: str,
        use_existing_file: bool = None,
        totp_secret_key: str = None,
        totp_length: str = None,
        totp_period: str = None,
        use_existing_totp_secret: bool = None,
        api_type: str = None,
        authenticated: bool = None,
        local_auth_test: bool = None,
        totp_field_attribute: str = None,
        totp_field_value: str = None,
        recording_username_field: str = None,
        recording_password_field: str = None,
        recording_display_name: str = None,
        use_existing_recording_password: bool = None,
        configuration_file: str = None,
        recording_file: str = None,
    ) -> bool:
        """PUT /authSession/file — update the auth session's config file
        (ZAP config) or recording file (Zest script).

        Args:
            uuid (str): The auth session's UUID. Required.
            environment_id (str): UUID of the Environment. Required.
            method (str): CONFIG or RECORDING. Required.
            use_existing_file (bool, optional): Keep the previously
                uploaded file instead of uploading a new one.
            totp_secret_key (str, optional): TOTP secret key.
            totp_length (str, optional): TOTP code length.
            totp_period (str, optional): TOTP refresh period, in seconds.
            use_existing_totp_secret (bool, optional): Keep the previously
                stored TOTP secret.
            api_type (str, optional): OPENAPI, POSTMAN, HAR, SOAP, or
                GRAPHQL, if the environment also has an API definition.
            authenticated (bool, optional): Whether the uploaded recording
                is already known to be authenticated.
            local_auth_test (bool, optional): Whether to run the auth test
                from the local (non-tunneled) network.
            totp_field_attribute (str, optional): Form field attribute
                the TOTP code should be entered into (RECORDING method).
            totp_field_value (str, optional): Form field value selector
                for the TOTP field (RECORDING method).
            recording_username_field (str, optional): The username value
                selected from the Zest recording.
            recording_password_field (str, optional): The password value
                selected from the Zest recording.
            recording_display_name (str, optional): Optional display name
                shown on screen after login.
            use_existing_recording_password (bool, optional): Keep the
                previously stored recording password; must leave
                recording_password_field empty when True.
            configuration_file (str, optional): Local path to the ZAP
                config file. Required when method=CONFIG unless
                use_existing_file=True.
            recording_file (str, optional): Local path to the Zest
                recording file. Required when method=RECORDING unless
                use_existing_file=True.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        data = {
            "UUID": uuid,
            "EnvironmentID": environment_id,
            "Method": method,
            "UseExistingFile": use_existing_file,
            "TOTPSecretKey": totp_secret_key,
            "TOTPLength": totp_length,
            "TOTPPeriod": totp_period,
            "UseExistingTOTPSecret": use_existing_totp_secret,
            "APIType": api_type,
            "Authenticated": authenticated,
            "LocalAuthTest": local_auth_test,
            "TOTPFieldAttribute": totp_field_attribute,
            "TOTPFieldValue": totp_field_value,
            "RecordingUsernameField": recording_username_field,
            "RecordingPasswordField": recording_password_field,
            "RecordingDisplayName": recording_display_name,
            "UseExistingRecordingPassword": use_existing_recording_password,
        }
        data = {k: str(v) for k, v in data.items() if v is not None}

        files = {}
        if configuration_file:
            with open(configuration_file, "rb") as fh:
                content = fh.read()
            files["configurationFile"] = (
                os.path.basename(configuration_file), content, "application/octet-stream"
            )
        if recording_file:
            with open(recording_file, "rb") as fh:
                content = fh.read()
            files["recordingFile"] = (
                os.path.basename(recording_file), content, "application/octet-stream"
            )

        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/file",
            data=data, files=files,
        )
        return 200 <= response.status_code < 300

    def get_auth_session(
        self, env_id: str, uuid: str = None, auth_success: str = None
    ) -> DastAuthSession:
        """GET /authSession/{envId} — get the full auth session for an
        Environment, including credentials and files.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str, optional): A specific auth session UUID, if the
                Environment has more than one on record.
            auth_success (str, optional): Filter by last auth test result.

        Returns:
            DastAuthSession
        """
        params = {"uuid": uuid, "authSuccess": auth_success}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}", params=params,
        )
        return DastAuthSession.from_dict(response.json())

    def get_auth_session_api_file(
        self, env_id: str, auth_session_uuid: str = None, file_uuid: str = None
    ) -> bytes:
        """GET /authSession/{envId}/apiFile — download an auth session's
        API definition file.

        Args:
            env_id (str): UUID of the Environment. Required.
            auth_session_uuid (str, optional): A specific auth session UUID.
            file_uuid (str, optional): A specific file's UUID, if more
                than one API file is attached.

        Returns:
            bytes: raw file content.
        """
        params = {"authSessionUUID": auth_session_uuid, "fileUUID": file_uuid}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/apiFile",
            params=params,
        )
        return response.content

    def delete_auth_session_api_file(self, env_id: str, api_file_id: str) -> bool:
        """DELETE /authSession/{envId}/apiFile/{apiFileId} — delete one of
        the auth session's API definition files.

        Args:
            env_id (str): UUID of the Environment. Required.
            api_file_id (str): UUID of the API file to delete. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=f"{self.base_url}/authSession/{env_id}/apiFile/{api_file_id}",
        )
        return 200 <= response.status_code < 300

    def get_auth_session_api_files_data(
        self, env_id: str, auth_session_uuid: str = None
    ) -> List[DastApiFileWithType]:
        """GET /authSession/{envId}/apiFilesData — get all of the auth
        session's API definition files, with their content.

        Args:
            env_id (str): UUID of the Environment. Required.
            auth_session_uuid (str, optional): A specific auth session UUID.

        Returns:
            List[DastApiFileWithType]
        """
        params = {"authSessionUUID": auth_session_uuid}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/apiFilesData",
            params=params,
        )
        return [
            DastApiFileWithType.from_dict(f)
            for f in (response.json().get("apiFiles") or [])
        ]

    def get_auth_session_diagnostics(self, env_id: str) -> bytes:
        """GET /authSession/{envId}/diagnostics — download a zip of
        diagnostics for the auth session.

        Confirmed live: 404s ("no auth diagnostics found") on a session
        straight off create_auth_session — see update_auth_session_api_file's
        docstring for the same "settle the session's method first" quirk.

        Args:
            env_id (str): UUID of the Environment. Required.

        Returns:
            bytes: raw ZIP file content.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/diagnostics"
        )
        return response.content

    def get_auth_session_domains(
        self, env_id: str, uuid: str = None
    ) -> List[str]:
        """GET /authSession/{envId}/domains — get the domains visited
        while setting up the auth session.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str, optional): A specific auth session UUID.

        Returns:
            List[str]: domains.
        """
        params = {"uuid": uuid}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/domains",
            params=params,
        )
        return response.json().get("domains", [])

    def get_auth_session_masked(
        self, env_id: str, uuid: str = None, auth_success: str = None
    ) -> DastAuthSession:
        """GET /authSession/{envId}/masked — get the auth session with
        credentials redacted (password, TOTP secret) and no file content.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str, optional): A specific auth session UUID.
            auth_success (str, optional): Filter by last auth test result.

        Returns:
            DastAuthSession
        """
        params = {"uuid": uuid, "authSuccess": auth_success}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/masked",
            params=params,
        )
        return DastAuthSession.from_dict(response.json())

    def set_auth_session_no_auth(self, env_id: str, uuid: str) -> bool:
        """PUT /authSession/{envId}/noAuth — switch the auth session to
        no-auth.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/{env_id}/noAuth",
            json={"UUID": uuid},
        )
        return 200 <= response.status_code < 300

    def ping_auth_session(self, env_id: str, uuid: str, source: str) -> bool:
        """PUT /authSession/{envId}/ping — ping the auth session to check
        whether the opposite side (browser/CLI) is still connected.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.
            source (str): Identifies which side is pinging. Required.
                Same undocumented-value situation as SessionType on
                create_auth_session; "CLI" is confirmed to work live
                (ping on an already-finished session 409s, which is
                expected and documented, not a validation rejection).

        Returns:
            bool: whether the opposite side is connected.
        """
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/{env_id}/ping",
            json={"UUID": uuid, "Source": source},
        )
        return response.json()

    def update_auth_session_report(
        self, env_id: str, uuid: str, test_log: str, report: str = None
    ) -> bool:
        """PUT /authSession/{envId}/report — upload the auth session's
        report and test log files.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.
            test_log (str): Local path to the test log file. Required.
            report (str, optional): Local path to the report file.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        with open(test_log, "rb") as fh:
            test_log_content = fh.read()
        files = {
            "testLog": (os.path.basename(test_log), test_log_content, "text/plain"),
        }
        if report:
            with open(report, "rb") as fh:
                report_content = fh.read()
            files["report"] = (
                os.path.basename(report), report_content, "application/octet-stream"
            )
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/authSession/{env_id}/report",
            data={"UUID": uuid}, files=files,
        )
        return 200 <= response.status_code < 300

    def get_auth_session_report(self, env_id: str, uuid: str) -> bytes:
        """GET /authSession/{envId}/report — download the auth session's
        report file.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.

        Returns:
            bytes: raw file content.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/report",
            params={"uuid": uuid},
        )
        return response.content

    def get_auth_session_report_data(
        self, env_id: str, uuid: str
    ) -> DastAuthSessionReportData:
        """GET /authSession/{envId}/reportData — get the auth session's
        report as structured data.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.

        Returns:
            DastAuthSessionReportData
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/reportData",
            params={"uuid": uuid},
        )
        return DastAuthSessionReportData.from_dict(response.json())

    def get_auth_session_state(self, env_id: str, uuid: str) -> Optional[str]:
        """GET /authSession/{envId}/state — get the auth session's current
        state.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.

        Returns:
            Optional[str]: the auth session's state.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/state",
            params={"uuid": uuid},
        )
        return response.json().get("state")

    def get_auth_session_test_log(self, env_id: str, uuid: str) -> bytes:
        """GET /authSession/{envId}/testLog — download the auth session's
        test log file.

        Args:
            env_id (str): UUID of the Environment. Required.
            uuid (str): The auth session's UUID. Required.

        Returns:
            bytes: raw file content.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/authSession/{env_id}/testLog",
            params={"uuid": uuid},
        )
        return response.content

    # ----- Tunnels -----
    #
    # A tunnel gives DAST a path into an Environment on a private network
    # (via the zrok-based agent). Gated behind a feature flag on some
    # tenants -- confirmed live to 503 "Service unavailable" when disabled.

    def create_tunnel(
        self, name: str, environment_id: str, url: str, description: str = None
    ) -> DastCreateTunnelResponse:
        """POST /tunnel — create a new tunnel for an Environment.

        Args:
            name (str): The tunnel's name. Required.
            environment_id (str): UUID of the Environment. Required.
            url (str): The local URL the tunnel exposes. Required.
            description (str, optional): A description for the tunnel.

        Returns:
            DastCreateTunnelResponse
        """
        body = {
            "name": name,
            "environmentId": environment_id,
            "url": url,
            "description": description,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/tunnel", json=body,
        )
        return DastCreateTunnelResponse.from_dict(response.json())

    def delete_tunnel_without_id(self) -> None:
        """DELETE /tunnel/ — always returns 400 (no tunnel id supplied).

        Included for completeness; there's no reason to call this —
        use delete_tunnel(id) instead. Raises the same ValueError every
        other non-2xx response raises (via check_response).
        """
        self.api_client.call_api(method="DELETE", url=f"{self.base_url}/tunnel/")

    def delete_tunnel(self, id: str) -> bool:
        """DELETE /tunnel/{id} — delete a tunnel.

        Args:
            id (str): The tunnel's ID. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/tunnel/{id}"
        )
        return 200 <= response.status_code < 300

    def get_tunnel(self, tunnel_id: str) -> DastTunnelResponse:
        """GET /tunnel/{tunnelId} — get a tunnel by ID.

        Args:
            tunnel_id (str): The tunnel's UUID. Required.

        Returns:
            DastTunnelResponse
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/tunnel/{tunnel_id}"
        )
        return DastTunnelResponse.from_dict(response.json())

    def get_tunnel_by_name(self, name: str) -> DastTunnelResponse:
        """GET /tunnelByName/{name} — get a tunnel by name.

        Args:
            name (str): The tunnel's name. Required.

        Returns:
            DastTunnelResponse
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/tunnelByName/{name}"
        )
        return DastTunnelResponse.from_dict(response.json())

    def get_tunnels(self) -> DastTunnelsResponse:
        """GET /tunnels — get all tunnels the caller can view.

        Returns:
            DastTunnelsResponse
        """
        response = self.api_client.call_api(method="GET", url=f"{self.base_url}/tunnels")
        return DastTunnelsResponse.from_dict(response.json())

    # ----- Sequences -----
    #
    # A sequence is an ordered chain of recordings (see Recordings below)
    # that DAST replays together, e.g. to script a multi-step login flow.

    def create_sequence(
        self, environment_id: str, name: str, recording_ids: List[str]
    ) -> DastSequence:
        """POST /sequences — create a sequence from existing recordings.

        Args:
            environment_id (str): UUID of the Environment. Required.
            name (str): The sequence's name. Required.
            recording_ids (List[str]): UUIDs of the recordings to chain
                together, in order. Required.

        Returns:
            DastSequence
        """
        body = {
            "environmentId": environment_id,
            "name": name,
            "recordingIds": recording_ids,
        }
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/sequences", json=body,
        )
        return DastSequence.from_dict(response.json())

    def delete_sequences(self, environment_id: str, sequence_ids: List[str]) -> bool:
        """DELETE /sequences — delete sequences by ID.

        Args:
            environment_id (str): UUID of the Environment. Required.
            sequence_ids (List[str]): UUIDs of the sequences to delete.
                Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        body = {"environmentId": environment_id, "sequenceIds": sequence_ids}
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/sequences", json=body,
        )
        return 200 <= response.status_code < 300

    def update_sequences_order(
        self, environment_id: str, sequence_ids: List[str]
    ) -> bool:
        """PUT /sequences/order — reorder an Environment's sequences.

        Args:
            environment_id (str): UUID of the Environment. Required.
            sequence_ids (List[str]): All of the environment's sequence
                UUIDs, in the desired order. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        body = {"environmentId": environment_id, "sequenceIds": sequence_ids}
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/sequences/order", json=body,
        )
        return 200 <= response.status_code < 300

    def update_sequence(
        self,
        sequence_id: str,
        environment_id: str,
        name: str,
        recording_ids: List[str],
    ) -> DastSequence:
        """PUT /sequences/{sequenceId} — update a sequence's name and/or
        recordings.

        Confirmed live: the update itself works (verified via
        get_sequence_recordings), but unlike the POST /sequences response,
        this endpoint's response always comes back with an empty
        recording_ids — not a sign the update failed.

        Args:
            sequence_id (str): UUID of the sequence to update. Required.
            environment_id (str): UUID of the Environment. Required.
            name (str): The sequence's new name. Required.
            recording_ids (List[str]): UUIDs of the recordings to chain
                together, in order. Required.

        Returns:
            DastSequence: note recording_ids is always empty here — see
                get_sequence_recordings for the actual current list.
        """
        body = {
            "environmentId": environment_id,
            "name": name,
            "recordingIds": recording_ids,
        }
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/sequences/{sequence_id}", json=body,
        )
        return DastSequence.from_dict(response.json())

    def get_sequence_scripts(self, env_id: str) -> DastSequenceScriptsResponse:
        """GET /environments/{envId}/sequence-scripts — get the
        environment's sequences as ordered recording-filename chains,
        plus a zip archive of the recording files, for CLI use.

        Args:
            env_id (str): UUID of the Environment. Required.

        Returns:
            DastSequenceScriptsResponse
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments/{env_id}/sequence-scripts"
        )
        return DastSequenceScriptsResponse.from_dict(response.json())

    def get_sequences(self, env_id: str) -> List[DastSequenceWithRecordingCount]:
        """GET /environments/{envId}/sequences — get an environment's
        sequences.

        Args:
            env_id (str): UUID of the Environment. Required.

        Returns:
            List[DastSequenceWithRecordingCount]
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments/{env_id}/sequences"
        )
        return [
            DastSequenceWithRecordingCount.from_dict(s)
            for s in (response.json() or [])
        ]

    def duplicate_sequence(self, env_id: str, sequence_id: str) -> DastSequence:
        """POST /environments/{envId}/sequences/{sequenceId}/duplicate —
        duplicate a sequence (name, recordings) and place the copy right
        after the source sequence.

        Args:
            env_id (str): UUID of the Environment. Required.
            sequence_id (str): UUID of the sequence to duplicate. Required.

        Returns:
            DastSequence: the newly created copy.
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/environments/{env_id}/sequences/{sequence_id}/duplicate",
        )
        return DastSequence.from_dict(response.json())

    def get_sequence_recordings(
        self, env_id: str, sequence_id: str
    ) -> List[DastRecordingWithPosition]:
        """GET /environments/{envId}/sequences/{sequenceId}/recordings —
        get the recordings making up a sequence, in order.

        Args:
            env_id (str): UUID of the Environment. Required.
            sequence_id (str): UUID of the sequence. Required.

        Returns:
            List[DastRecordingWithPosition]
        """
        response = self.api_client.call_api(
            method="GET",
            url=(
                f"{self.base_url}/environments/{env_id}/sequences/"
                f"{sequence_id}/recordings"
            ),
        )
        return [
            DastRecordingWithPosition.from_dict(r) for r in (response.json() or [])
        ]

    # ----- Recordings -----
    #
    # A recording is a single scripted interaction (a Zest/HAR-style
    # capture) that sequences chain together.

    def create_recordings(
        self,
        environment_id: str,
        files: List[str],
        metadata: List[Dict[str, str]],
    ) -> List[DastRecording]:
        """POST /recordings — upload one or more recording files.

        Confirmed live: the server matches each uploaded file to its
        metadata entry by the file's multipart filename, which must
        equal that entry's "name" — not by upload order or local
        filename, despite the spec's plain `files: [binary]` array
        shape giving no indication of this. This method handles that
        for you (the actual local filenames in `files` don't matter).

        Each file must also be genuine Zest (JSON) recording content;
        a non-Zest file 400s with "failed to process ZST file content".

        Args:
            environment_id (str): UUID of the Environment. Required.
            files (List[str]): Local paths of the recording files to
                upload. Required.
            metadata (List[Dict[str, str]]): One {"name": ...,
                "description": ...} entry per `files` entry, in the same
                order. Required.

        Returns:
            List[DastRecording]
        """
        data = {
            "environmentId": environment_id,
            "metadata": json.dumps(metadata),
        }
        file_fields = []
        for path, meta in zip(files, metadata):
            with open(path, "rb") as fh:
                content = fh.read()
            file_fields.append(
                ("files", (meta["name"], content, "application/octet-stream"))
            )
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/recordings",
            data=data, files=file_fields,
        )
        return [DastRecording.from_dict(r) for r in (response.json() or [])]

    def delete_recordings(
        self, environment_id: str, recording_ids: List[str]
    ) -> bool:
        """DELETE /recordings — delete recordings (file, DB row, and from
        any sequence they're part of).

        Args:
            environment_id (str): UUID of the Environment. Required.
            recording_ids (List[str]): UUIDs of the recordings to delete.
                Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        body = {"environmentId": environment_id, "recordingIds": recording_ids}
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/recordings", json=body,
        )
        return 200 <= response.status_code < 300

    def update_recording(
        self,
        recording_id: str,
        environment_id: str,
        name: str = None,
        description: str = None,
        file: str = None,
    ) -> DastRecording:
        """PUT /recordings/{recordingId} — update a recording's name,
        description, and/or underlying file.

        Args:
            recording_id (str): UUID of the recording to update. Required.
            environment_id (str): UUID of the Environment. Required.
            name (str, optional): The recording's new name.
            description (str, optional): The recording's new description.
            file (str, optional): Local path to a replacement .zst
                recording file.

        Returns:
            DastRecording
        """
        data = {
            "environmentId": environment_id,
            "name": name,
            "description": description,
        }
        data = {k: v for k, v in data.items() if v is not None}
        files = {}
        if file:
            with open(file, "rb") as fh:
                content = fh.read()
            files["file"] = (os.path.basename(file), content, "application/octet-stream")
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/recordings/{recording_id}",
            data=data, files=files,
        )
        return DastRecording.from_dict(response.json())

    def get_environment_recordings(
        self, env_id: str, from_: int = None, to: int = None
    ) -> DastRecordingsCollection:
        """GET /environments/{envId}/recordings — get an environment's
        recordings.

        Args:
            env_id (str): UUID of the Environment. Required.
            from_ (int, optional): Pagination start offset. (Trailing
                underscore avoids shadowing the built-in `from`.)
            to (int, optional): Pagination end offset.

        Returns:
            DastRecordingsCollection
        """
        params = {"from": from_, "to": to}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/environments/{env_id}/recordings",
            params=params,
        )
        return DastRecordingsCollection.from_dict(response.json())

    def save_proxy_recorder_file(self, env_id: str, proxy_recorder_file: str) -> bool:
        """PUT /environments/{envId}/proxyRecorderFile — save a
        proxy-recorder HAR file for an environment.

        Confirmed live: despite the spec calling this a ".zst compressed
        HAR file", "zst" here means Zest (as everywhere else in this
        auth/recording surface), not Zstandard compression — the server
        rejects it with "failed to parse zst JSON" if the content isn't
        plain JSON. The exact expected JSON shape (presumably Zest-
        wrapped HAR data) isn't confirmed.

        Args:
            env_id (str): UUID of the Environment. Required.
            proxy_recorder_file (str): Local path to the file. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        with open(proxy_recorder_file, "rb") as fh:
            content = fh.read()
        files = {
            "proxyRecorderFile": (
                os.path.basename(proxy_recorder_file), content, "application/octet-stream"
            )
        }
        response = self.api_client.call_api(
            method="PUT",
            url=f"{self.base_url}/environments/{env_id}/proxyRecorderFile",
            files=files,
        )
        return 200 <= response.status_code < 300

    # ----- Correlations -----
    #
    # A correlations scan cross-references DAST findings against SAST/SCA
    # projects to confirm whether a given vulnerability is actually
    # reachable/exploitable. Gated behind a feature flag and a credits
    # balance -- confirmed live to 503 when disabled, and the spec
    # documents 402 "Payment required" when credits are insufficient.

    def get_correlations_enabled(self) -> DastFlagEnabled:
        """GET /correlations/enabled — whether correlations scans are
        enabled for the tenant.

        Returns:
            DastFlagEnabled
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/correlations/enabled"
        )
        return DastFlagEnabled.from_dict(response.json())

    def create_correlations_scan(
        self,
        environment_id: str,
        scan_id: str,
        similarity_ids: List[DastSimilarityIds],
        projects: List[dict] = None,
        project_uploads: List[dict] = None,
        source: str = None,
    ) -> str:
        """POST /correlations/scan — create a correlations scan.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the DAST scan whose findings to
                correlate. Required.
            similarity_ids (List[DastSimilarityIds]): The findings to
                correlate. Required.
            projects (List[dict], optional): SAST/SCA projects to
                correlate against (CorrelationProject shape: projectId
                required, plus sourceId or scanId). Passed through as
                raw dicts — not modeled as a DTO here.
            project_uploads (List[dict], optional): Projects to correlate
                against an ad-hoc upload (ProjectUploadPayload shape).
                Passed through as raw dicts.
            source (str, optional): Caller identifier.

        Returns:
            str: the new correlations scan's ID (plain-text response body).
        """
        body = {
            "environmentId": environment_id,
            "scanId": scan_id,
            "similarityIds": [s.to_dict() for s in similarity_ids],
            "projects": projects,
            "projectUploads": project_uploads,
            "source": source,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/correlations/scan", json=body,
        )
        return response.text.strip().strip('"')

    def delete_correlations_scan(self, scan_id: str) -> str:
        """DELETE /correlations/scan/{scanId} — delete a correlations scan.

        Args:
            scan_id (str): UUID of the correlations scan. Required.

        Returns:
            str: the API's plain-text response body.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/correlations/scan/{scan_id}"
        )
        return response.text.strip().strip('"')

    def cancel_correlations_scan(self, scan_id: str) -> str:
        """PATCH /correlations/scan/{scanId} — cancel a correlations scan.

        Args:
            scan_id (str): UUID of the correlations scan. Required.

        Returns:
            str: the API's plain-text response body.
        """
        response = self.api_client.call_api(
            method="PATCH", url=f"{self.base_url}/correlations/scan/{scan_id}"
        )
        return response.text.strip().strip('"')

    def get_correlations_scan_status(
        self, scan_id: str, environment_id: str
    ) -> Optional[str]:
        """GET /correlations/scan/{scanId}/status — get a correlations
        scan's status.

        Args:
            scan_id (str): UUID of the correlations scan. Required.
            environment_id (str): UUID of the Environment. Required.

        Returns:
            Optional[str]: the correlations scan's status.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/correlations/scan/{scan_id}/status",
            params={"environmentId": environment_id},
        )
        return response.json().get("status")

    def get_correlations_scans(
        self,
        environment_id: str,
        scan_id: str = None,
        correlation_id: str = None,
        filter_: dict = None,
        sort: List[str] = None,
        search: str = None,
        from_: int = None,
        to: int = None,
    ) -> DastCorrelationScansCollection:
        """GET /correlations/scans — get correlations scans.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str, optional): Filter by DAST scan UUID.
            correlation_id (str, optional): Filter by correlations scan UUID.
            filter_ (dict, optional): Partial-match filter. Supported
                keys: initiator (str), projectIds (List[str]),
                source (List[str]), status (List[str]). (Trailing
                underscore avoids shadowing the built-in `filter`.)
            sort (List[str], optional): Columns to sort by.
            search (str, optional): Free-text search.
            from_ (int, optional): Pagination start offset. (Trailing
                underscore avoids shadowing the built-in `from`.)
            to (int, optional): Pagination end offset.

        Returns:
            DastCorrelationScansCollection
        """
        params = {
            "environmentId": environment_id,
            "scanId": scan_id,
            "correlationId": correlation_id,
            "sort": sort,
            "search": search,
            "from": from_,
            "to": to,
        }
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/correlations/scans", params=params,
        )
        return DastCorrelationScansCollection.from_dict(response.json())

    # ----- Pentest -----
    #
    # A pentest scan runs an AI-driven penetration test against a DAST
    # environment's findings. Same gating pattern as correlations: a
    # feature flag (503 when disabled) and a credits balance (402 when
    # insufficient).

    def get_pentest_enabled(self) -> DastFlagEnabled:
        """GET /pentest/enabled — whether AI pentester is enabled for the
        tenant.

        Returns:
            DastFlagEnabled
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/pentest/enabled"
        )
        return DastFlagEnabled.from_dict(response.json())

    def create_pentest_scan(
        self,
        environment_id: str,
        scan_id: str,
        similarity_ids: List[DastSimilarityIds],
        settings: DastPentestScanSettings,
        source: str = None,
    ) -> str:
        """POST /pentest/scan — create a pentest scan.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the DAST scan whose findings to
                pentest. Required.
            similarity_ids (List[DastSimilarityIds]): The findings to
                pentest. Required.
            settings (DastPentestScanSettings): The pentest's plan mode,
                attack profile, and path filters. Required.
            source (str, optional): Caller identifier.

        Returns:
            str: the new pentest scan's ID (plain-text response body).
        """
        body = {
            "environmentId": environment_id,
            "scanId": scan_id,
            "similarityIds": [s.to_dict() for s in similarity_ids],
            "settings": settings.to_dict(),
            "source": source,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/pentest/scan", json=body,
        )
        return response.text.strip().strip('"')

    def cancel_pentest_scan(self, scan_id: str) -> str:
        """PATCH /pentest/scan/{scanId} — cancel a pentest scan.

        Args:
            scan_id (str): UUID of the pentest scan. Required.

        Returns:
            str: the API's plain-text response body.
        """
        response = self.api_client.call_api(
            method="PATCH", url=f"{self.base_url}/pentest/scan/{scan_id}"
        )
        return response.text.strip().strip('"')

    def delete_pentest_scan(self, scan_id: str) -> str:
        """DELETE /pentest/scan/{scanId} — delete a pentest scan.

        Args:
            scan_id (str): UUID of the pentest scan. Required.

        Returns:
            str: the API's plain-text response body.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/pentest/scan/{scan_id}"
        )
        return response.text.strip().strip('"')

    def get_pentest_scans(
        self,
        environment_id: str,
        scan_id: str = None,
        pentest_scan_id: str = None,
        filter_: dict = None,
        sort: List[str] = None,
        search: str = None,
        from_: int = None,
        to: int = None,
    ) -> DastPentestScansCollection:
        """GET /pentest/scans — get pentest scans.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str, optional): Filter by DAST scan UUID.
            pentest_scan_id (str, optional): Filter by pentest scan UUID.
            filter_ (dict, optional): Partial-match filter. Supported
                keys: initiator (str), source (List[str]),
                status (List[str]). (Trailing underscore avoids
                shadowing the built-in `filter`.)
            sort (List[str], optional): Columns to sort by.
            search (str, optional): Free-text search.
            from_ (int, optional): Pagination start offset. (Trailing
                underscore avoids shadowing the built-in `from`.)
            to (int, optional): Pagination end offset.

        Returns:
            DastPentestScansCollection
        """
        params = {
            "environmentId": environment_id,
            "scanId": scan_id,
            "pentestScanId": pentest_scan_id,
            "sort": sort,
            "search": search,
            "from": from_,
            "to": to,
        }
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/pentest/scans", params=params,
        )
        return DastPentestScansCollection.from_dict(response.json())

    # ----- Credits -----
    #
    # Correlations and pentest scans (and possibly other actions) consume
    # a shared tenant-level credits balance.

    def get_credit_action_rates(self) -> dict:
        """GET /credits/action-rates — get how many credits each action
        costs.

        Returns:
            dict: raw response body. The spec documents this as an
            untyped object with no fixed shape.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/credits/action-rates"
        )
        return response.json()

    def get_credit_balance(self) -> dict:
        """GET /credits/balance — get the tenant's current credits balance.

        Returns:
            dict: raw response body. The spec documents this as an
            untyped object with no fixed shape.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/credits/balance"
        )
        return response.json()

    def get_correlation_capacity(self) -> DastCorrelationCapacityResponse:
        """GET /credits/correlation-capacity — get the tenant's remaining
        correlation-scan capacity.

        Returns:
            DastCorrelationCapacityResponse
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/credits/correlation-capacity"
        )
        return DastCorrelationCapacityResponse.from_dict(response.json())

    def deduct_credits(
        self,
        environment_id: str,
        risk_names: List[str],
        metadata: Dict[str, str] = None,
    ) -> dict:
        """POST /credits/deduct — deduct credits for an action.

        Args:
            environment_id (str): UUID of the Environment. Required.
            risk_names (List[str]): Names of the risks/actions being
                charged for. Required.
            metadata (Dict[str, str], optional): Additional metadata to
                record with the deduction.

        Returns:
            dict: raw response body. The spec documents this as an
            untyped object with no fixed shape.
        """
        body = {
            "environment_id": environment_id,
            "risk_names": risk_names,
            "metadata": metadata,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/credits/deduct", json=body,
        )
        return response.json()

    def get_pentest_max_profile(self) -> DastPentestMaxProfile:
        """GET /credits/pentest-max-profile — get the maximum attack
        profile the tenant can afford for pentest scans.

        Confirmed live on a tenant with AI pentester disabled: 500
        "failed to get pentest max profile", not the 503 that every other
        gated endpoint in this file returns when its feature is off.

        Returns:
            DastPentestMaxProfile
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/credits/pentest-max-profile"
        )
        return DastPentestMaxProfile.from_dict(response.json())

    # ----- Pipeline -----
    #
    # A pipeline tracks a multi-step CI/CD-driven scan workflow for an
    # Environment (as opposed to the ad-hoc run_scan/run_public_scan
    # flow). Only one pipeline operation may be in progress per
    # Environment at a time -- the spec documents 409 otherwise.

    def create_pipeline(
        self, environment_id: str, cancel_older_pipelines: bool = None
    ) -> str:
        """POST /pipeline — create a pipeline for an Environment.

        Args:
            environment_id (str): UUID of the Environment. Required.
            cancel_older_pipelines (bool, optional): Whether to cancel
                any other pipeline already running for this Environment.

        Returns:
            str: the new pipeline's ID (plain-text response body).
        """
        body = {
            "environmentId": environment_id,
            "cancelOlderPipelines": cancel_older_pipelines,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/pipeline", json=body,
        )
        return response.text.strip().strip('"')

    def update_pipeline(
        self,
        id: str,
        environment_id: str,
        current_step_type: str,
        current_step_id: str,
    ) -> str:
        """PUT /pipeline/{id} — advance a pipeline to its next step.

        Args:
            id (str): UUID of the pipeline. Required.
            environment_id (str): UUID of the Environment. Required.
            current_step_type (str): The pipeline step type now in
                progress. Required.
            current_step_id (str): UUID identifying the current step
                (e.g. a scan ID). Required.

        Returns:
            str: the API's plain-text response body.
        """
        body = {
            "environmentId": environment_id,
            "currentStepType": current_step_type,
            "currentStepId": current_step_id,
        }
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/pipeline/{id}", json=body,
        )
        return response.text.strip().strip('"')

    def delete_pipeline(self, id: str, environment_id: str) -> str:
        """DELETE /pipeline/{id} — delete a pipeline.

        Confirmed live: despite the spec listing no parameters at all for
        this endpoint (and no request body), it 400s with "environmentId
        query parameter is required" unless environment_id is passed as
        a query param.

        Args:
            id (str): UUID of the pipeline. Required.
            environment_id (str): UUID of the Environment. Required
                (despite the spec not documenting this parameter).

        Returns:
            str: the API's plain-text response body.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/pipeline/{id}",
            params={"environmentId": environment_id},
        )
        return response.text.strip().strip('"')

    # ----- Application association -----
    #
    # Links DAST Environments to CxOne Applications, independently of
    # an Environment's own `applications`/project_ids fields.

    def associate_apps_with_environment(
        self, env_id: str, application_ids: List[str]
    ) -> bool:
        """POST /associateApps/{envId} — associate Applications with an
        Environment.

        Args:
            env_id (str): UUID of the Environment. Required.
            application_ids (List[str]): UUIDs of the Applications to
                associate. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/associateApps/{env_id}",
            json={"ApplicationIDs": application_ids},
        )
        return 200 <= response.status_code < 300

    def associate_envs_with_application(
        self,
        app_id: str,
        environment_ids: List[str],
        primary_environment_id: str = None,
    ) -> bool:
        """POST /associateEnvs/{appId} — associate Environments with an
        Application.

        Args:
            app_id (str): UUID of the Application. Required.
            environment_ids (List[str]): UUIDs of the Environments to
                associate. Required.
            primary_environment_id (str, optional): UUID to set as the
                Application's primary Environment; must also be included
                in `environment_ids`.

        Returns:
            bool: the API's response body (itself a bare boolean).
        """
        body = {
            "EnvironmentIDs": environment_ids,
            "PrimaryEnvironmentID": primary_environment_id,
        }
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/associateEnvs/{app_id}", json=body,
        )
        return response.json()

    def get_associated_apps(
        self, env_id: str
    ) -> List[DastApplicationEnvironmentWithPrimary]:
        """GET /associatedApps/{envId} — get the Applications associated
        with an Environment.

        Args:
            env_id (str): UUID of the Environment. Required.

        Returns:
            List[DastApplicationEnvironmentWithPrimary]
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/associatedApps/{env_id}"
        )
        return [
            DastApplicationEnvironmentWithPrimary.from_dict(a)
            for a in (response.json() or [])
        ]

    def get_associated_envs(
        self, app_id: str, primary: bool = None
    ) -> List[DastApplicationEnvironmentInfo]:
        """GET /associatedEnvs/{appId} — get the Environments associated
        with an Application.

        Args:
            app_id (str): UUID of the Application. Required.
            primary (bool, optional): Only return the primary
                Environment.

        Returns:
            List[DastApplicationEnvironmentInfo]
        """
        params = {}
        if primary is not None:
            params["primary"] = "true" if primary else "false"
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/associatedEnvs/{app_id}",
            params=params,
        )
        return [
            DastApplicationEnvironmentInfo.from_dict(e)
            for e in (response.json() or [])
        ]

    def disassociate_apps_from_environment(
        self, env_id: str, application_ids: List[str]
    ) -> bool:
        """DELETE /disassociateApps/{envId} — disassociate Applications
        from an Environment.

        Args:
            env_id (str): UUID of the Environment. Required.
            application_ids (List[str]): UUIDs of the Applications to
                disassociate. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/disassociateApps/{env_id}",
            json={"ApplicationIDs": application_ids},
        )
        return 200 <= response.status_code < 300

    def disassociate_envs_from_application(
        self, app_id: str, environment_ids: List[str]
    ) -> bool:
        """DELETE /disassociateEnvs/{appId} — disassociate Environments
        from an Application.

        Args:
            app_id (str): UUID of the Application. Required.
            environment_ids (List[str]): UUIDs of the Environments to
                disassociate. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE", url=f"{self.base_url}/disassociateEnvs/{app_id}",
            json={"EnvironmentIDs": environment_ids},
        )
        return 200 <= response.status_code < 300


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


def get_scans(
    environment_id: str,
    filter_: DastScanFilter = None,
    from_: int = None,
    groups: List[str] = None,
    last_status: List[DastScanStatus] = None,
    match: DastScanFilter = None,
    search: str = None,
    sort: List[DastScanSortBy] = None,
    tags: List[str] = None,
    to: int = None,
) -> DastScansCollection:
    return DastScanAPI().get_scans(
        environment_id=environment_id, filter_=filter_, from_=from_,
        groups=groups, last_status=last_status, match=match,
        search=search, sort=sort, tags=tags, to=to,
    )


def run_scan(scan: DastRunScanInput) -> str:
    return DastScanAPI().run_scan(scan=scan)


def run_public_scan(environment_id: str) -> str:
    return DastScanAPI().run_public_scan(environment_id=environment_id)


def update_scan(scan: DastScanUpdate) -> str:
    return DastScanAPI().update_scan(scan=scan)


def dast_cancel_scan(scan_id: str, environment_id: str) -> bool:
    return DastScanAPI().cancel_scan(scan_id=scan_id, environment_id=environment_id)


def dast_delete_scan(scan_id: str, environment_id: str) -> bool:
    return DastScanAPI().delete_scan(scan_id=scan_id, environment_id=environment_id)


def get_scans_count_by_group(
    environment_id: str,
    group_by: List[DastScanGroupBy] = None,
    filter_: DastScanGroupFilter = None,
    groups: List[str] = None,
    last_scan_status: List[DastScanStatus] = None,
    search: str = None,
    tags: List[str] = None,
) -> List[DastScanGroupCount]:
    return DastScanAPI().get_scans_count_by_group(
        environment_id=environment_id, group_by=group_by, filter_=filter_,
        groups=groups, last_scan_status=last_scan_status,
        search=search, tags=tags,
    )


def dast_get_scan_by_id(scan_id: str) -> DastScan:
    return DastScanAPI().get_scan_by_id(scan_id=scan_id)


def get_scan_log(scan_id: str) -> bytes:
    return DastScanAPI().get_scan_log(scan_id=scan_id)


def create_auth_session(
    environment_id: str,
    session_type: str,
    url: str,
    uuid: str = None,
    method: str = None,
) -> bool:
    return DastScanAPI().create_auth_session(
        environment_id=environment_id, session_type=session_type, url=url,
        uuid=uuid, method=method,
    )


def update_auth_session_api_file(
    uuid: str,
    environment_id: str,
    api_file: str,
    api_type: str = None,
    api_url: str = None,
    api_variables: Dict[str, str] = None,
) -> str:
    return DastScanAPI().update_auth_session_api_file(
        uuid=uuid, environment_id=environment_id, api_file=api_file,
        api_type=api_type, api_url=api_url, api_variables=api_variables,
    )


def validate_auth_session_api_file(api_file: str, api_type: str = None) -> dict:
    return DastScanAPI().validate_auth_session_api_file(
        api_file=api_file, api_type=api_type,
    )


def bulk_replace_auth_session_api_files(
    environment_id: str,
    auth_session_uuid: str = None,
    files: List[str] = None,
    api_types: List[str] = None,
    api_variables: List[Dict[str, str]] = None,
    api_urls: List[str] = None,
    file_ids_to_keep: List[str] = None,
    kept_files_updates: Dict[str, dict] = None,
) -> List[str]:
    return DastScanAPI().bulk_replace_auth_session_api_files(
        environment_id=environment_id, auth_session_uuid=auth_session_uuid,
        files=files, api_types=api_types, api_variables=api_variables,
        api_urls=api_urls, file_ids_to_keep=file_ids_to_keep,
        kept_files_updates=kept_files_updates,
    )


def update_auth_session_credentials(
    uuid: str,
    environment_id: str,
    login_page_url: str,
    user_name: str,
    password: str = None,
    use_existing_password: bool = None,
    totp: DastAuthSessionTotp = None,
    use_existing_totp_secret: bool = None,
    local_auth_test: bool = None,
    totp_field: DastTotpField = None,
) -> bool:
    return DastScanAPI().update_auth_session_credentials(
        uuid=uuid, environment_id=environment_id, login_page_url=login_page_url,
        user_name=user_name, password=password,
        use_existing_password=use_existing_password, totp=totp,
        use_existing_totp_secret=use_existing_totp_secret,
        local_auth_test=local_auth_test, totp_field=totp_field,
    )


def update_auth_session_file(
    uuid: str,
    environment_id: str,
    method: str,
    use_existing_file: bool = None,
    totp_secret_key: str = None,
    totp_length: str = None,
    totp_period: str = None,
    use_existing_totp_secret: bool = None,
    api_type: str = None,
    authenticated: bool = None,
    local_auth_test: bool = None,
    totp_field_attribute: str = None,
    totp_field_value: str = None,
    recording_username_field: str = None,
    recording_password_field: str = None,
    recording_display_name: str = None,
    use_existing_recording_password: bool = None,
    configuration_file: str = None,
    recording_file: str = None,
) -> bool:
    return DastScanAPI().update_auth_session_file(
        uuid=uuid, environment_id=environment_id, method=method,
        use_existing_file=use_existing_file, totp_secret_key=totp_secret_key,
        totp_length=totp_length, totp_period=totp_period,
        use_existing_totp_secret=use_existing_totp_secret, api_type=api_type,
        authenticated=authenticated, local_auth_test=local_auth_test,
        totp_field_attribute=totp_field_attribute,
        totp_field_value=totp_field_value,
        recording_username_field=recording_username_field,
        recording_password_field=recording_password_field,
        recording_display_name=recording_display_name,
        use_existing_recording_password=use_existing_recording_password,
        configuration_file=configuration_file, recording_file=recording_file,
    )


def get_auth_session(
    env_id: str, uuid: str = None, auth_success: str = None
) -> DastAuthSession:
    return DastScanAPI().get_auth_session(
        env_id=env_id, uuid=uuid, auth_success=auth_success,
    )


def get_auth_session_api_file(
    env_id: str, auth_session_uuid: str = None, file_uuid: str = None
) -> bytes:
    return DastScanAPI().get_auth_session_api_file(
        env_id=env_id, auth_session_uuid=auth_session_uuid, file_uuid=file_uuid,
    )


def delete_auth_session_api_file(env_id: str, api_file_id: str) -> bool:
    return DastScanAPI().delete_auth_session_api_file(
        env_id=env_id, api_file_id=api_file_id,
    )


def get_auth_session_api_files_data(
    env_id: str, auth_session_uuid: str = None
) -> List[DastApiFileWithType]:
    return DastScanAPI().get_auth_session_api_files_data(
        env_id=env_id, auth_session_uuid=auth_session_uuid,
    )


def get_auth_session_diagnostics(env_id: str) -> bytes:
    return DastScanAPI().get_auth_session_diagnostics(env_id=env_id)


def get_auth_session_domains(env_id: str, uuid: str = None) -> List[str]:
    return DastScanAPI().get_auth_session_domains(env_id=env_id, uuid=uuid)


def get_auth_session_masked(
    env_id: str, uuid: str = None, auth_success: str = None
) -> DastAuthSession:
    return DastScanAPI().get_auth_session_masked(
        env_id=env_id, uuid=uuid, auth_success=auth_success,
    )


def set_auth_session_no_auth(env_id: str, uuid: str) -> bool:
    return DastScanAPI().set_auth_session_no_auth(env_id=env_id, uuid=uuid)


def ping_auth_session(env_id: str, uuid: str, source: str) -> bool:
    return DastScanAPI().ping_auth_session(env_id=env_id, uuid=uuid, source=source)


def update_auth_session_report(
    env_id: str, uuid: str, test_log: str, report: str = None
) -> bool:
    return DastScanAPI().update_auth_session_report(
        env_id=env_id, uuid=uuid, test_log=test_log, report=report,
    )


def get_auth_session_report(env_id: str, uuid: str) -> bytes:
    return DastScanAPI().get_auth_session_report(env_id=env_id, uuid=uuid)


def get_auth_session_report_data(
    env_id: str, uuid: str
) -> DastAuthSessionReportData:
    return DastScanAPI().get_auth_session_report_data(env_id=env_id, uuid=uuid)


def get_auth_session_state(env_id: str, uuid: str) -> Optional[str]:
    return DastScanAPI().get_auth_session_state(env_id=env_id, uuid=uuid)


def get_auth_session_test_log(env_id: str, uuid: str) -> bytes:
    return DastScanAPI().get_auth_session_test_log(env_id=env_id, uuid=uuid)


def create_tunnel(
    name: str, environment_id: str, url: str, description: str = None
) -> DastCreateTunnelResponse:
    return DastScanAPI().create_tunnel(
        name=name, environment_id=environment_id, url=url, description=description,
    )


def delete_tunnel_without_id() -> None:
    return DastScanAPI().delete_tunnel_without_id()


def delete_tunnel(id: str) -> bool:
    return DastScanAPI().delete_tunnel(id=id)


def get_tunnel(tunnel_id: str) -> DastTunnelResponse:
    return DastScanAPI().get_tunnel(tunnel_id=tunnel_id)


def get_tunnel_by_name(name: str) -> DastTunnelResponse:
    return DastScanAPI().get_tunnel_by_name(name=name)


def get_tunnels() -> DastTunnelsResponse:
    return DastScanAPI().get_tunnels()


def create_sequence(
    environment_id: str, name: str, recording_ids: List[str]
) -> DastSequence:
    return DastScanAPI().create_sequence(
        environment_id=environment_id, name=name, recording_ids=recording_ids,
    )


def delete_sequences(environment_id: str, sequence_ids: List[str]) -> bool:
    return DastScanAPI().delete_sequences(
        environment_id=environment_id, sequence_ids=sequence_ids,
    )


def update_sequences_order(environment_id: str, sequence_ids: List[str]) -> bool:
    return DastScanAPI().update_sequences_order(
        environment_id=environment_id, sequence_ids=sequence_ids,
    )


def update_sequence(
    sequence_id: str, environment_id: str, name: str, recording_ids: List[str]
) -> DastSequence:
    return DastScanAPI().update_sequence(
        sequence_id=sequence_id, environment_id=environment_id, name=name,
        recording_ids=recording_ids,
    )


def get_sequence_scripts(env_id: str) -> DastSequenceScriptsResponse:
    return DastScanAPI().get_sequence_scripts(env_id=env_id)


def get_sequences(env_id: str) -> List[DastSequenceWithRecordingCount]:
    return DastScanAPI().get_sequences(env_id=env_id)


def duplicate_sequence(env_id: str, sequence_id: str) -> DastSequence:
    return DastScanAPI().duplicate_sequence(env_id=env_id, sequence_id=sequence_id)


def get_sequence_recordings(
    env_id: str, sequence_id: str
) -> List[DastRecordingWithPosition]:
    return DastScanAPI().get_sequence_recordings(
        env_id=env_id, sequence_id=sequence_id,
    )


def create_recordings(
    environment_id: str, files: List[str], metadata: List[Dict[str, str]]
) -> List[DastRecording]:
    return DastScanAPI().create_recordings(
        environment_id=environment_id, files=files, metadata=metadata,
    )


def delete_recordings(environment_id: str, recording_ids: List[str]) -> bool:
    return DastScanAPI().delete_recordings(
        environment_id=environment_id, recording_ids=recording_ids,
    )


def update_recording(
    recording_id: str,
    environment_id: str,
    name: str = None,
    description: str = None,
    file: str = None,
) -> DastRecording:
    return DastScanAPI().update_recording(
        recording_id=recording_id, environment_id=environment_id, name=name,
        description=description, file=file,
    )


def get_environment_recordings(
    env_id: str, from_: int = None, to: int = None
) -> DastRecordingsCollection:
    return DastScanAPI().get_environment_recordings(env_id=env_id, from_=from_, to=to)


def save_proxy_recorder_file(env_id: str, proxy_recorder_file: str) -> bool:
    return DastScanAPI().save_proxy_recorder_file(
        env_id=env_id, proxy_recorder_file=proxy_recorder_file,
    )


def get_correlations_enabled() -> DastFlagEnabled:
    return DastScanAPI().get_correlations_enabled()


def create_correlations_scan(
    environment_id: str,
    scan_id: str,
    similarity_ids: List[DastSimilarityIds],
    projects: List[dict] = None,
    project_uploads: List[dict] = None,
    source: str = None,
) -> str:
    return DastScanAPI().create_correlations_scan(
        environment_id=environment_id, scan_id=scan_id, similarity_ids=similarity_ids,
        projects=projects, project_uploads=project_uploads, source=source,
    )


def delete_correlations_scan(scan_id: str) -> str:
    return DastScanAPI().delete_correlations_scan(scan_id=scan_id)


def cancel_correlations_scan(scan_id: str) -> str:
    return DastScanAPI().cancel_correlations_scan(scan_id=scan_id)


def get_correlations_scan_status(scan_id: str, environment_id: str) -> Optional[str]:
    return DastScanAPI().get_correlations_scan_status(
        scan_id=scan_id, environment_id=environment_id,
    )


def get_correlations_scans(
    environment_id: str,
    scan_id: str = None,
    correlation_id: str = None,
    filter_: dict = None,
    sort: List[str] = None,
    search: str = None,
    from_: int = None,
    to: int = None,
) -> DastCorrelationScansCollection:
    return DastScanAPI().get_correlations_scans(
        environment_id=environment_id, scan_id=scan_id, correlation_id=correlation_id,
        filter_=filter_, sort=sort, search=search, from_=from_, to=to,
    )


def get_pentest_enabled() -> DastFlagEnabled:
    return DastScanAPI().get_pentest_enabled()


def create_pentest_scan(
    environment_id: str,
    scan_id: str,
    similarity_ids: List[DastSimilarityIds],
    settings: DastPentestScanSettings,
    source: str = None,
) -> str:
    return DastScanAPI().create_pentest_scan(
        environment_id=environment_id, scan_id=scan_id, similarity_ids=similarity_ids,
        settings=settings, source=source,
    )


def cancel_pentest_scan(scan_id: str) -> str:
    return DastScanAPI().cancel_pentest_scan(scan_id=scan_id)


def delete_pentest_scan(scan_id: str) -> str:
    return DastScanAPI().delete_pentest_scan(scan_id=scan_id)


def get_pentest_scans(
    environment_id: str,
    scan_id: str = None,
    pentest_scan_id: str = None,
    filter_: dict = None,
    sort: List[str] = None,
    search: str = None,
    from_: int = None,
    to: int = None,
) -> DastPentestScansCollection:
    return DastScanAPI().get_pentest_scans(
        environment_id=environment_id, scan_id=scan_id, pentest_scan_id=pentest_scan_id,
        filter_=filter_, sort=sort, search=search, from_=from_, to=to,
    )


def get_credit_action_rates() -> dict:
    return DastScanAPI().get_credit_action_rates()


def get_credit_balance() -> dict:
    return DastScanAPI().get_credit_balance()


def get_correlation_capacity() -> DastCorrelationCapacityResponse:
    return DastScanAPI().get_correlation_capacity()


def deduct_credits(
    environment_id: str, risk_names: List[str], metadata: Dict[str, str] = None
) -> dict:
    return DastScanAPI().deduct_credits(
        environment_id=environment_id, risk_names=risk_names, metadata=metadata,
    )


def get_pentest_max_profile() -> DastPentestMaxProfile:
    return DastScanAPI().get_pentest_max_profile()


def create_pipeline(environment_id: str, cancel_older_pipelines: bool = None) -> str:
    return DastScanAPI().create_pipeline(
        environment_id=environment_id, cancel_older_pipelines=cancel_older_pipelines,
    )


def update_pipeline(
    id: str, environment_id: str, current_step_type: str, current_step_id: str
) -> str:
    return DastScanAPI().update_pipeline(
        id=id, environment_id=environment_id, current_step_type=current_step_type,
        current_step_id=current_step_id,
    )


def delete_pipeline(id: str, environment_id: str) -> str:
    return DastScanAPI().delete_pipeline(id=id, environment_id=environment_id)


def associate_apps_with_environment(env_id: str, application_ids: List[str]) -> bool:
    return DastScanAPI().associate_apps_with_environment(
        env_id=env_id, application_ids=application_ids,
    )


def associate_envs_with_application(
    app_id: str, environment_ids: List[str], primary_environment_id: str = None
) -> bool:
    return DastScanAPI().associate_envs_with_application(
        app_id=app_id, environment_ids=environment_ids,
        primary_environment_id=primary_environment_id,
    )


def get_associated_apps(env_id: str) -> List[DastApplicationEnvironmentWithPrimary]:
    return DastScanAPI().get_associated_apps(env_id=env_id)


def get_associated_envs(
    app_id: str, primary: bool = None
) -> List[DastApplicationEnvironmentInfo]:
    return DastScanAPI().get_associated_envs(app_id=app_id, primary=primary)


def disassociate_apps_from_environment(env_id: str, application_ids: List[str]) -> bool:
    return DastScanAPI().disassociate_apps_from_environment(
        env_id=env_id, application_ids=application_ids,
    )


def disassociate_envs_from_application(app_id: str, environment_ids: List[str]) -> bool:
    return DastScanAPI().disassociate_envs_from_application(
        app_id=app_id, environment_ids=environment_ids,
    )
