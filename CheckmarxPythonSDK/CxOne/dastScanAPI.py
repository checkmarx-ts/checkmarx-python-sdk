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
    DastRunScanInput,
    DastScan,
    DastScanFilter,
    DastScanGroupBy,
    DastScanGroupCount,
    DastScanGroupFilter,
    DastScanSortBy,
    DastScanStatus,
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
