"""DAST Results Service REST API.

Endpoints under <server>/api/dast/mfe-results. Endpoints with
documented response shapes return DTO objects; the rest are stubs
that return the raw parsed JSON response until their schemas are
pinned down.
"""
import json
import os
from typing import List, Optional
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    DastAlertInfo,
    DastAlertInstanceSummarizedList,
    DastAlertLevelOccurrencesResponse,
    DastAlertLevelResultList,
    DastComplianceAnalytics,
    DastComplianceOverTimeResponse,
    DastGroups,
    DastManualFindingInstanceResultList,
    DastManualFindingsAlertLevelResultList,
    DastPentestFindingResult,
    DastResultDetail,
    DastResultsChangelogInput,
    DastResultsCollection,
    DastResultsFilter,
    DastResultsGroupBy,
    DastResultsGroupCount,
    DastResultsSortBy,
    DastResultsStatesSummary,
    DastRiskLevelOverTimeResponse,
    DastScreenshot,
    DastStatesOverTimeResponse,
    DastTimeSpanRiskSummary,
    DastTopFiveRisks,
    DastVulnerabilitySummary,
)


def _flatten_filter(name: str, obj_filter) -> dict:
    """Expand a filter DTO into bracketed nested query params
    (e.g. filter[severity]=HIGH) — the wire format the DAST APIs use."""
    if obj_filter is None:
        return {}
    return {f"{name}[{k}]": v for k, v in obj_filter.to_dict().items()}


class DastResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/dast/mfe-results"
        )

    def dast_get_results(
        self,
        scan_id: str,
        filter_: DastResultsFilter = None,
        page: int = None,
        per_page: int = None,
        search: str = None,
        sort_by: List[DastResultsSortBy] = None,
        group: str = None,
    ) -> DastResultsCollection:
        """GET /results/{scan_id} — paged results (risks) identified by
        a specific DAST scan.

        Args:
            scan_id (str): UUID of the scan.
            filter_ (DastResultsFilter, optional): partial-match filter
                on severity, path, name, method, status, state, url,
                owasp, alert_similarity_id.
            page (int, optional): 1-based page number. Default 1.
            per_page (int, optional): page size, 1-100. Default 10.
            search (str, optional): substring search across multiple
                columns.
            sort_by (list of DastResultsSortBy, optional): sort columns.
                Each entry is serialized as "<col>:asc"; pass a raw
                "col:desc" string for per-column descending order.
            group (str, optional): filter by groups.

        Returns:
            DastResultsCollection
        """
        params = {
            "page": page,
            "per_page": per_page,
            "search": search,
            "sort_by": (
                [s if ":" in str(s) else f"{s.value if isinstance(s, DastResultsSortBy) else s}:asc"
                 for s in sort_by]
                if sort_by else None
            ),
            "group": group,
        }
        params.update(_flatten_filter("filter", filter_))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}",
            params=params,
        )
        return DastResultsCollection.from_dict(response.json())

    def update_results(self, changelog: DastResultsChangelogInput) -> bool:
        """POST /changelog — update severity/state/notes on one or more
        results (single or batch).

        Args:
            changelog (DastResultsChangelogInput): the update payload.
                similarity_id_2 / environment_id / scan_id are required;
                severity / state / note / type / alert_similarity_id /
                custom_state_id are optional. When type=ALERT,
                alert_similarity_id is required.

        Returns:
            bool: True if the API returned a 2xx status. Response body
            is plain-text "OK" on success.
        """
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/changelog",
            json=changelog.to_dict(),
        )
        return 200 <= response.status_code < 300

    def get_result_info(self, result_id: str, scan_id: str) -> DastResultDetail:
        """GET /results/info/{result_id}/{scan_id} — detailed info about
        a specific result.

        Doc shows the response wrapped as {"results": {...}}, but live
        returns the fields at the top level. Unwraps defensively in
        case the API ever matches the doc.

        Args:
            result_id (str): UUID of the result.
            scan_id (str): UUID of the scan it belongs to.

        Returns:
            DastResultDetail
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/info/{result_id}/{scan_id}",
        )
        data = response.json()
        # Doc says wrapped under "results"; live returns flat. Handle both.
        if isinstance(data, dict) and isinstance(data.get("results"), dict):
            data = data["results"]
        return DastResultDetail.from_dict(data)

    def get_results_count_by_group(
        self,
        scan_id: str,
        group_by: List[DastResultsGroupBy] = None,
        filter_: DastResultsFilter = None,
        search: str = None,
    ) -> List[DastResultsGroupCount]:
        """GET /results/{scan_id}/group — count of results per group.

        Args:
            scan_id (str): UUID of the scan.
            group_by (list of DastResultsGroupBy, optional): columns to
                group by. The wire param is `group` (singular) — this
                SDK uses `group_by` for consistency with sibling
                endpoints.
            filter_ (DastResultsFilter, optional): partial-match filter
                (severity, name, method, status, state, url, path,
                owasp). alert_similarity_id is on the shared DTO but
                ignored by this endpoint.
            search (str, optional): substring search.

        Returns:
            list of DastResultsGroupCount. Each bucket has `count` and
            `group` (a list of values — one entry per group_by column
            in the order they were requested).
        """
        params = {
            "group": (
                [g.value if isinstance(g, DastResultsGroupBy) else g for g in group_by]
                if group_by else None
            ),
            "search": search,
        }
        params.update(_flatten_filter("filter", filter_))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}/group",
            params=params,
        )
        return [DastResultsGroupCount.from_dict(b) for b in (response.json() or [])]

    def health_check(self) -> str:
        """GET / — service health check.

        Confirmed live: despite the spec declaring Content-Type
        application/json, the body is a plain unquoted string -- not
        valid JSON. Returns response.text, not response.json().

        Returns:
            str: e.g. "Result-Service V2 V3 MFE Server Working!"
        """
        response = self.api_client.call_api(method="GET", url=self.base_url)
        return response.text

    # ----- Alert-level results -----

    def get_alert_info(self, environment_id: str, scan_id: str, alert_id: str) -> DastAlertInfo:
        """GET /results/environment/{environment_id}/{scan_id}/alert/{alert_id}/info
        — get an alert's description/info.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            alert_id (str): The alert similarity ID. Required.

        Returns:
            DastAlertInfo
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/alert/{alert_id}/info",
        )
        return DastAlertInfo.from_dict(response.json())

    def get_alert_instances(
        self,
        environment_id: str,
        scan_id: str,
        alert_id: str,
        page: int,
        per_page: int,
        sort_by: List[str] = None,
        search: str = None,
        filter_: dict = None,
    ) -> DastAlertInstanceSummarizedList:
        """GET .../alert/{alert_id}/instances — get an alert's instances,
        paginated/filtered/sorted/searched.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            alert_id (str): The alert similarity ID. Required.
            page (int): Page number. Required.
            per_page (int): Page size. Required.
            sort_by (List[str], optional): e.g. ["severity:desc"].
            search (str, optional): Free-text search.
            filter_ (dict, optional): Partial-match filter (AlertLevelFilter
                shape: severity, name, method, status, state, url, path,
                owasp, alert_similarity_id, correlation_findings, source,
                attack_findings). (Trailing underscore avoids shadowing
                the built-in `filter`.)

        Returns:
            DastAlertInstanceSummarizedList
        """
        params = {"page": page, "per_page": per_page, "sort_by": sort_by, "search": search}
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/alert/{alert_id}/instances",
            params=params,
        )
        return DastAlertInstanceSummarizedList.from_dict(response.json())

    def get_alert_level_results(
        self,
        environment_id: str,
        scan_id: str,
        page: int,
        per_page: int,
        sort_by: List[str] = None,
        search: str = None,
        filter_: dict = None,
    ) -> DastAlertLevelResultList:
        """GET .../{scan_id}/alert_level — get results grouped by alert
        (one row per alert, with its instance count).

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            page (int): Page number. Required.
            per_page (int): Page size. Required.
            sort_by (List[str], optional): e.g. ["severity:desc"].
            search (str, optional): Free-text search.
            filter_ (dict, optional): See get_alert_instances.

        Returns:
            DastAlertLevelResultList
        """
        params = {"page": page, "per_page": per_page, "sort_by": sort_by, "search": search}
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/alert_level",
            params=params,
        )
        return DastAlertLevelResultList.from_dict(response.json())

    def post_alert_level_results(
        self, environment_id: str, scan_id: str, body: dict = None
    ) -> DastAlertLevelResultList:
        """POST .../{scan_id}/alert_level — same as get_alert_level_results,
        but with the filter/sort/search/group options in a JSON body
        instead of the query string (useful when `filter`/`group` would
        make the query string too long).

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            body (dict, optional): AlertLevelRequestBody shape: page,
                per_page, sort_by (List[str]), search, filter (dict),
                group (dict).

        Returns:
            DastAlertLevelResultList
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/alert_level",
            json=body or {},
        )
        return DastAlertLevelResultList.from_dict(response.json())

    def get_grouped_alert_level_results(
        self,
        environment_id: str,
        scan_id: str,
        group: List[str],
        search: str = None,
        filter_: dict = None,
    ) -> List[DastGroups]:
        """GET .../{scan_id}/alert_level/group — get alert-level results
        grouped by the requested columns, with a count per tuple.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            group (List[str]): Columns to group by (status, name, method,
                severity, url, path, state, compliance, owasp). Max 10.
                Required.
            search (str, optional): Free-text search.
            filter_ (dict, optional): See get_alert_instances.

        Returns:
            List[DastGroups]
        """
        params = {"group": group, "search": search}
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/alert_level/group",
            params=params,
        )
        return [DastGroups.from_dict(g) for g in (response.json() or [])]

    def post_grouped_alert_level_results(
        self, environment_id: str, scan_id: str, body: dict
    ) -> List[DastGroups]:
        """POST .../{scan_id}/alert_level/group — same as
        get_grouped_alert_level_results, but with the group/filter/search
        options in a JSON body instead of the query string.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            body (dict): GroupByRequestBody shape: group (List[str],
                required), search, filter (dict). Required.

        Returns:
            List[DastGroups]
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/alert_level/group",
            json=body,
        )
        return [DastGroups.from_dict(g) for g in (response.json() or [])]

    def get_full_scan_results(self, environment_id: str, scan_id: str) -> dict:
        """GET .../{scan_id}/full_scan_results — get every alert and
        instance for a scan (used by the correlation wizard), including
        correlatedAt timestamps.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.

        Returns:
            dict: raw response body (GetScanResultsResponse) -- left
            unmodeled; this is a large, all-alerts-and-instances payload
            for UI/wizard consumption.
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/full_scan_results",
        )
        return response.json()

    def get_vulnerability_summary(
        self, environment_id: str, scan_id: str
    ) -> DastVulnerabilitySummary:
        """GET .../{scan_id}/vulnerability_summary — get a scan's
        vulnerability summary (severity/state/compliance breakdowns).

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.

        Returns:
            DastVulnerabilitySummary
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/vulnerability_summary",
        )
        return DastVulnerabilitySummary.from_dict(response.json())

    def is_alert_level_enabled(self) -> Optional[bool]:
        """GET /results/setting/alert_level_enabled — whether alert-level
        grouping is enabled for the caller's tenant.

        Returns:
            Optional[bool]
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/setting/alert_level_enabled"
        )
        return response.json().get("isEnabled")

    # ----- Scan-level summaries -----

    def get_aging_summary(self, scan_id: str) -> DastTimeSpanRiskSummary:
        """GET /results/{scan_id}/aging_summary — get risk counts
        bucketed by age for a scan.

        Args:
            scan_id (str): UUID of the scan. Required.

        Returns:
            DastTimeSpanRiskSummary
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}/aging_summary"
        )
        return DastTimeSpanRiskSummary.from_dict(response.json())

    def get_instance_findings(
        self, scan_id: str, environment_id: str, similarity_id_2: str
    ) -> dict:
        """GET /results/{scan_id}/environment/{environment_id}/instance/{similarity_id_2}
        — get full finding data (request/response, params, evidence) for
        a specific instance.

        Args:
            scan_id (str): UUID of the scan. Required.
            environment_id (str): UUID of the Environment. Required.
            similarity_id_2 (str): The instance similarity ID. Required.

        Returns:
            dict: raw response body (InstanceFindings) -- left unmodeled.
        """
        response = self.api_client.call_api(
            method="GET",
            url=(
                f"{self.base_url}/results/{scan_id}/environment/"
                f"{environment_id}/instance/{similarity_id_2}"
            ),
        )
        return response.json()

    def get_top_five_risks(
        self, scan_id: str, severity: str = None
    ) -> List[DastTopFiveRisks]:
        """GET /results/{scan_id}/top_five_risks — get the top five risk
        categories for a scan.

        Args:
            scan_id (str): UUID of the scan. Required.
            severity (str, optional): Filter to a specific severity.

        Returns:
            List[DastTopFiveRisks]
        """
        params = {}
        if severity:
            params["filter[severity]"] = severity
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}/top_five_risks",
            params=params,
        )
        return [DastTopFiveRisks.from_dict(r) for r in (response.json() or [])]

    def get_scan_sites_tree(self, environment_id: str, scan_id: str) -> List[dict]:
        """GET /sitestree/{environment_id}/{scan_id} — get a scan's
        sites tree.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.

        Returns:
            List[dict]: raw response body (SiteTreeResponse items) --
            left unmodeled; a recursive tree structure.
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/sitestree/{environment_id}/{scan_id}"
        )
        return response.json() or []

    def get_results_states_summary(self, app_id: str) -> Optional[DastResultsStatesSummary]:
        """GET /states_summary/{app_id} — get the results-states summary
        for an Application.

        Confirmed live: 204 No Content (empty body) for an Application
        with no DAST Environments associated, rather than a
        zero-valued object. check_response() treats any GET 204 as an
        error (only 200/401 are allowed for GET), so that specific case
        is caught here and turned into a clean None return.

        Args:
            app_id (str): UUID of the Application. Required.

        Returns:
            Optional[DastResultsStatesSummary]: None if the Application
                has no DAST data.
        """
        try:
            response = self.api_client.call_api(
                method="GET", url=f"{self.base_url}/states_summary/{app_id}"
            )
        except ValueError as e:
            if "204" in str(e):
                return None
            raise
        if not response.text:
            return None
        return DastResultsStatesSummary.from_dict(response.json())

    # ----- Analytics & overview (time series) -----

    def get_compliance_analytics(self, app_id: str) -> Optional[DastComplianceAnalytics]:
        """GET /analytics/compliance/{app_id} — get compliance pass/fail
        counts for an Application.

        Confirmed live: 204 No Content (empty body) for an Application
        with no DAST Environments associated, rather than a
        zero-valued object. check_response() treats any GET 204 as an
        error (only 200/401 are allowed for GET), so that specific case
        is caught here and turned into a clean None return.

        Args:
            app_id (str): The Application ID. Required.

        Returns:
            Optional[DastComplianceAnalytics]: None if the Application
                has no DAST data.
        """
        try:
            response = self.api_client.call_api(
                method="GET", url=f"{self.base_url}/analytics/compliance/{app_id}"
            )
        except ValueError as e:
            if "204" in str(e):
                return None
            raise
        if not response.text:
            return None
        return DastComplianceAnalytics.from_dict(response.json())

    def get_latest_correlation_results(
        self, environment_id: str, scan_id: str, similarity_id: str, type: str
    ) -> dict:
        """GET /correlations/{environment_id}/{scan_id}/results/latest —
        get the latest code-correlation results for an alert or instance.

        Requires the DAST-code correlation feature flag to be enabled
        for the tenant; 403s otherwise.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            similarity_id (str): The alert or instance similarity ID to
                get correlation results for. Required.
            type (str): "alert" or "instance" -- what `similarity_id`
                refers to. Required.

        Returns:
            dict: raw response body (VulnerabilityCorrelations) -- left
            unmodeled.
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/correlations/{environment_id}/{scan_id}/results/latest",
            params={"similarity_id": similarity_id, "type": type},
        )
        return response.json()

    def get_compliance_over_time(
        self,
        environment_id: str,
        start_date: str,
        end_date: str,
        risk_levels: List[str] = None,
        compliance_types: List[str] = None,
    ) -> DastComplianceOverTimeResponse:
        """GET /overview/compliance_over_time/{environment_id} — get
        vulnerability counts over time, broken down by compliance type.

        Args:
            environment_id (str): UUID of the Environment. Required.
            start_date (str): Start of the period (RFC3339). Required.
            end_date (str): End of the period (RFC3339). Required.
            risk_levels (List[str], optional): CRITICAL/HIGH/MEDIUM/LOW/INFO.
            compliance_types (List[str], optional): OWASP/CWE/WASC.

        Returns:
            DastComplianceOverTimeResponse
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "risk_levels": risk_levels,
            "compliance_types": compliance_types,
        }
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/overview/compliance_over_time/{environment_id}",
            params=params,
        )
        return DastComplianceOverTimeResponse.from_dict(response.json())

    def get_occurrences_over_time(
        self,
        environment_id: str,
        scan_id: str = None,
        start: str = None,
        end: str = None,
        severity: List[str] = None,
        compliance: List[str] = None,
        include_manual_results: bool = None,
    ) -> DastAlertLevelOccurrencesResponse:
        """GET /overview/occurrences_over_time/{environment_id} — get
        new-vs-recurrent occurrence counts over time.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str, optional): Filter to one scan.
            start (str, optional): Start of the period (RFC3339).
            end (str, optional): End of the period (RFC3339).
            severity (List[str], optional): CRITICAL/HIGH/MEDIUM/LOW/INFO.
            compliance (List[str], optional): Compliance type filter.
            include_manual_results (bool, optional): Whether to include
                manual findings.

        Returns:
            DastAlertLevelOccurrencesResponse
        """
        params = {
            "scan_id": scan_id,
            "start": start,
            "end": end,
            "severity": severity,
            "compliance": compliance,
            "include_manual_results": include_manual_results,
        }
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/overview/occurrences_over_time/{environment_id}",
            params=params,
        )
        return DastAlertLevelOccurrencesResponse.from_dict(response.json())

    def get_risk_level_over_time(
        self,
        environment_id: str,
        start_date: str,
        end_date: str,
        risk_levels: List[str] = None,
        compliance_types: List[str] = None,
    ) -> DastRiskLevelOverTimeResponse:
        """GET /overview/risk_level_over_time/{environment_id} — get
        severity-breakdown vulnerability counts over time.

        Args:
            environment_id (str): UUID of the Environment. Required.
            start_date (str): Start of the period (RFC3339). Required.
            end_date (str): End of the period (RFC3339). Required.
            risk_levels (List[str], optional): CRITICAL/HIGH/MEDIUM/LOW/INFO.
            compliance_types (List[str], optional): OWASP/CWE/WASC.

        Returns:
            DastRiskLevelOverTimeResponse
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "risk_levels": risk_levels,
            "compliance_types": compliance_types,
        }
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/overview/risk_level_over_time/{environment_id}",
            params=params,
        )
        return DastRiskLevelOverTimeResponse.from_dict(response.json())

    def get_states_over_time(
        self,
        environment_id: str,
        start_date: str,
        end_date: str,
        risk_levels: List[str] = None,
        compliance_types: List[str] = None,
        include_manual_results: bool = None,
    ) -> DastStatesOverTimeResponse:
        """GET /overview/states_over_time/{environment_id} — get
        result-state-breakdown counts over time.

        Args:
            environment_id (str): UUID of the Environment. Required.
            start_date (str): Start of the period (RFC3339). Required.
            end_date (str): End of the period (RFC3339). Required.
            risk_levels (List[str], optional): CRITICAL/HIGH/MEDIUM/LOW/INFO.
            compliance_types (List[str], optional): OWASP/CWE/WASC.
            include_manual_results (bool, optional): Whether to include
                manual findings.

        Returns:
            DastStatesOverTimeResponse
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "risk_levels": risk_levels,
            "compliance_types": compliance_types,
            "include_manual_results": include_manual_results,
        }
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/overview/states_over_time/{environment_id}",
            params=params,
        )
        return DastStatesOverTimeResponse.from_dict(response.json())

    # ----- Manual findings -----
    #
    # A manual finding is a risk entered by a user (rather than detected
    # by DAST itself) against a scan's Environment.

    def get_manual_findings(
        self,
        environment_id: str,
        scan_id: str,
        alert_id: str = None,
        page: int = None,
        per_page: int = None,
        sort_by: List[str] = None,
        search: str = None,
        filter_: dict = None,
    ) -> DastManualFindingInstanceResultList:
        """GET .../{scan_id}/manual_findings — get manual-finding
        instances for a scan.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            alert_id (str, optional): Filter to one manual-finding alert.
            page (int, optional): Page number.
            per_page (int, optional): Page size.
            sort_by (List[str], optional): e.g. ["severity:desc"].
            search (str, optional): Free-text search.
            filter_ (dict, optional): See get_alert_instances.

        Returns:
            DastManualFindingInstanceResultList
        """
        params = {
            "alert_id": alert_id, "page": page, "per_page": per_page,
            "sort_by": sort_by, "search": search,
        }
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings",
            params=params,
        )
        return DastManualFindingInstanceResultList.from_dict(response.json())

    def create_manual_findings_batch(
        self,
        environment_id: str,
        scan_id: str,
        findings: List[dict],
        only_current_scan: bool = None,
    ) -> str:
        """POST /results/{environment_id}/{scan_id}/manual_findings —
        create a batch of manual findings.

        Note the path has no "environment/" segment, unlike every other
        manual_findings endpoint -- confirmed against the spec, not a typo.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            findings (List[dict]): One or more CreateFindingRequest
                objects. Required.
            only_current_scan (bool, optional): If True, the batch only
                applies to this scan and isn't carried forward to future
                scans.

        Returns:
            str: the new batch's ID.
        """
        body = {"findings": findings, "only_current_scan": only_current_scan}
        body = {k: v for k, v in body.items() if v is not None}
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/results/{environment_id}/{scan_id}/manual_findings",
            json=body,
        )
        return response.json().get("batch_id")

    def update_manual_finding_alert(
        self, environment_id: str, scan_id: str, update: dict
    ) -> bool:
        """PUT .../{scan_id}/manual_findings/alert — update a manual
        finding's alert-level fields (applies to all of its instances).

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            update (dict): UpdateManualFindingAlertRequest shape:
                result_id, severity, name, status required; note,
                description, compliance, resolution, confidence,
                cwe_id, wasc_id optional. Required.

                Confirmed live: despite the spec marking both `state`
                and `custom_state_id` as individually optional (only
                mutually exclusive with each other), the server
                actually requires one of them -- omitting both 400s
                with "state or custom_state_id is required".

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="PUT",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings/alert",
            json=update,
        )
        return 200 <= response.status_code < 300

    def get_manual_finding_alert_info(
        self, environment_id: str, scan_id: str, alert_id: str
    ) -> DastAlertInfo:
        """GET .../manual_findings/alert/{alert_id}/info — get a manual
        finding alert's description/info.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            alert_id (str): The manual finding alert ID. Required.

        Returns:
            DastAlertInfo
        """
        response = self.api_client.call_api(
            method="GET",
            url=(
                f"{self.base_url}/results/environment/{environment_id}/{scan_id}"
                f"/manual_findings/alert/{alert_id}/info"
            ),
        )
        return DastAlertInfo.from_dict(response.json())

    def update_manual_finding_alert_instance(
        self,
        environment_id: str,
        scan_id: str,
        update: dict,
        screenshots: List[str] = None,
        delete_screenshot_ids: List[str] = None,
    ) -> bool:
        """PUT .../manual_findings/alert_instance — update a manual
        finding alert together with one of its instances.

        Sends JSON when no screenshot changes are given; sends
        multipart/form-data (with `update` JSON-encoded under the
        `data` field) when screenshots or delete_screenshot_ids are
        given, per the spec's two accepted content types.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            update (dict): UpdateManualFindingAlertInstanceRequest
                shape: instance_id, severity, status, url, path, method
                required; description, compliance, resolution,
                confidence, cwe_id, wasc_id, note, evidence, attack,
                other_info, request/response header/body optional.
                Required.

                Confirmed live: despite the spec marking both `state`
                and `custom_state_id` as individually optional (only
                mutually exclusive with each other), the server
                actually requires one of them -- omitting both 400s
                with "state or custom_state_id is required".
            screenshots (List[str], optional): Local paths of screenshot
                files to upload (png/jpeg/gif/webp, max 10MiB each, max
                10 total per instance).
            delete_screenshot_ids (List[str], optional): IDs of existing
                screenshots to delete.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        url = (
            f"{self.base_url}/results/environment/{environment_id}/{scan_id}"
            f"/manual_findings/alert_instance"
        )
        if not screenshots and not delete_screenshot_ids:
            response = self.api_client.call_api(method="PUT", url=url, json=update)
            return 200 <= response.status_code < 300

        data = {"data": json.dumps(update)}
        if delete_screenshot_ids:
            data["delete_screenshot_ids"] = json.dumps(delete_screenshot_ids)
        file_fields = []
        for path in (screenshots or []):
            with open(path, "rb") as fh:
                content = fh.read()
            file_fields.append(("screenshots", (os.path.basename(path), content, "application/octet-stream")))
        response = self.api_client.call_api(
            method="PUT", url=url, data=data, files=file_fields,
        )
        return 200 <= response.status_code < 300

    def get_manual_findings_alert_level(
        self,
        environment_id: str,
        scan_id: str,
        page: int,
        per_page: int,
        sort_by: List[str] = None,
        search: str = None,
        filter_: dict = None,
    ) -> DastManualFindingsAlertLevelResultList:
        """GET .../manual_findings/alert_level — get manual findings
        grouped by alert (one row per alert, with its instance count).

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            page (int): Page number. Required.
            per_page (int): Page size. Required.
            sort_by (List[str], optional): e.g. ["severity:desc"].
            search (str, optional): Free-text search.
            filter_ (dict, optional): See get_alert_instances.

        Returns:
            DastManualFindingsAlertLevelResultList
        """
        params = {"page": page, "per_page": per_page, "sort_by": sort_by, "search": search}
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings/alert_level",
            params=params,
        )
        return DastManualFindingsAlertLevelResultList.from_dict(response.json())

    def get_grouped_manual_findings_alert_level(
        self,
        environment_id: str,
        scan_id: str,
        group: List[str],
        search: str = None,
        filter_: dict = None,
    ) -> List[DastGroups]:
        """GET .../manual_findings/alert_level/group — get manual
        findings grouped by the requested columns, with a count per tuple.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            group (List[str]): Columns to group by. Max 10. Required.
            search (str, optional): Free-text search.
            filter_ (dict, optional): See get_alert_instances.

        Returns:
            List[DastGroups]
        """
        params = {"group": group, "search": search}
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings/alert_level/group",
            params=params,
        )
        return [DastGroups.from_dict(g) for g in (response.json() or [])]

    def delete_manual_finding_alerts(
        self, environment_id: str, scan_id: str, alert_ids: List[str]
    ) -> bool:
        """DELETE .../manual_findings/alerts — delete manual finding
        alerts (and all of their instances).

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            alert_ids (List[str]): UUIDs of the alerts to delete.
                Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings/alerts",
            json={"alert_ids": alert_ids},
        )
        return 200 <= response.status_code < 300

    def get_grouped_manual_findings(
        self,
        environment_id: str,
        scan_id: str,
        group: List[str],
        search: str = None,
        filter_: dict = None,
    ) -> List[DastGroups]:
        """GET .../manual_findings/group — get manual finding instances
        grouped by the requested columns, with a count per tuple.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            group (List[str]): Columns to group by. Max 10. Required.
            search (str, optional): Free-text search.
            filter_ (dict, optional): See get_alert_instances.

        Returns:
            List[DastGroups]
        """
        params = {"group": group, "search": search}
        if filter_:
            params.update({f"filter[{k}]": v for k, v in filter_.items()})
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings/group",
            params=params,
        )
        return [DastGroups.from_dict(g) for g in (response.json() or [])]

    def update_manual_finding_instance(
        self,
        environment_id: str,
        scan_id: str,
        update: dict,
        screenshots: List[str] = None,
        delete_screenshot_ids: List[str] = None,
    ) -> bool:
        """PUT .../manual_findings/instance — update a single manual
        finding instance (not the whole alert).

        Same JSON-vs-multipart behavior as
        update_manual_finding_alert_instance.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            update (dict): UpdateManualFindingInstanceRequest shape:
                result_id, severity, status, url, path, method required;
                the rest optional (same fields as the alert_instance
                variant, minus instance_id/description/compliance/
                resolution/confidence/cwe_id/wasc_id). Required.

                Confirmed live: despite the spec marking both `state`
                and `custom_state_id` as individually optional (only
                mutually exclusive with each other), the server
                actually requires one of them -- omitting both 400s
                with "state or custom_state_id is required".
            screenshots (List[str], optional): Local paths of screenshot
                files to upload.
            delete_screenshot_ids (List[str], optional): IDs of existing
                screenshots to delete.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        url = (
            f"{self.base_url}/results/environment/{environment_id}/{scan_id}"
            f"/manual_findings/instance"
        )
        if not screenshots and not delete_screenshot_ids:
            response = self.api_client.call_api(method="PUT", url=url, json=update)
            return 200 <= response.status_code < 300

        data = {"data": json.dumps(update)}
        if delete_screenshot_ids:
            data["delete_screenshot_ids"] = json.dumps(delete_screenshot_ids)
        file_fields = []
        for path in (screenshots or []):
            with open(path, "rb") as fh:
                content = fh.read()
            file_fields.append(("screenshots", (os.path.basename(path), content, "application/octet-stream")))
        response = self.api_client.call_api(
            method="PUT", url=url, data=data, files=file_fields,
        )
        return 200 <= response.status_code < 300

    def get_manual_finding_instance_info(
        self, environment_id: str, scan_id: str, instance_id: str
    ) -> DastResultDetail:
        """GET .../manual_findings/instance/{instance_id}/info — get a
        manual finding instance's full detail.

        Reuses DastResultDetail -- ResultInfo is the identical shape to
        the ResultDetail schema get_result_info already returns.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            instance_id (str): UUID of the manual finding instance.
                Required.

        Returns:
            DastResultDetail
        """
        response = self.api_client.call_api(
            method="GET",
            url=(
                f"{self.base_url}/results/environment/{environment_id}/{scan_id}"
                f"/manual_findings/instance/{instance_id}/info"
            ),
        )
        return DastResultDetail.from_dict(response.json())

    def get_manual_finding_instance_screenshots(
        self, environment_id: str, scan_id: str, instance_id: str
    ) -> List[DastScreenshot]:
        """GET .../manual_findings/instance/{instance_id}/screenshots —
        get a manual finding instance's screenshots.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            instance_id (str): UUID of the manual finding instance.
                Required.

        Returns:
            List[DastScreenshot]
        """
        response = self.api_client.call_api(
            method="GET",
            url=(
                f"{self.base_url}/results/environment/{environment_id}/{scan_id}"
                f"/manual_findings/instance/{instance_id}/screenshots"
            ),
        )
        return [DastScreenshot.from_dict(s) for s in (response.json() or [])]

    def unlink_manual_findings(
        self, environment_id: str, scan_id: str, option: str
    ) -> bool:
        """POST .../manual_findings/unlink — unlink this scan's manual
        findings batch(es) from future scans.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            option (str): Which scans to unlink from: "current_scan",
                "current_and_future", or "active_from_next". Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/results/environment/{environment_id}/{scan_id}/manual_findings/unlink",
            json={"option": option},
        )
        return 200 <= response.status_code < 300

    def delete_manual_finding_instances(
        self, environment_id: str, scan_id: str, alert_id: str, instance_ids: List[str]
    ) -> bool:
        """DELETE .../manual_findings/{alert_id}/instances — delete
        specific instances of a manual finding alert.

        Args:
            environment_id (str): UUID of the Environment. Required.
            scan_id (str): UUID of the scan. Required.
            alert_id (str): The manual finding alert ID. Required.
            instance_ids (List[str]): UUIDs of the instances to delete.
                Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=(
                f"{self.base_url}/results/environment/{environment_id}/{scan_id}"
                f"/manual_findings/{alert_id}/instances"
            ),
            json={"instance_ids": instance_ids},
        )
        return 200 <= response.status_code < 300

    # ----- Instance screenshots -----

    def get_instance_screenshots(
        self, environment_id: str, similarity_id_2: str
    ) -> List[DastScreenshot]:
        """GET /results/environment/{environment_id}/instance/{similarity_id_2}/screenshots
        — get a DAST-detected instance's screenshots.

        Args:
            environment_id (str): UUID of the Environment. Required.
            similarity_id_2 (str): The instance similarity ID (lowercase
                hex). Required.

        Returns:
            List[DastScreenshot]
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/instance/{similarity_id_2}/screenshots",
        )
        return [DastScreenshot.from_dict(s) for s in (response.json() or [])]

    def upload_instance_screenshots(
        self, environment_id: str, similarity_id_2: str, screenshots: List[str]
    ) -> List[str]:
        """POST .../instance/{similarity_id_2}/screenshots — upload
        screenshots for a DAST-detected instance.

        Args:
            environment_id (str): UUID of the Environment. Required.
            similarity_id_2 (str): The instance similarity ID (lowercase
                hex). Required.
            screenshots (List[str]): Local paths of screenshot files
                (PNG/JPEG/GIF). Max 10 files, 10 MiB each. Required.

        Returns:
            List[str]: IDs of the uploaded screenshots.
        """
        file_fields = []
        for path in screenshots:
            with open(path, "rb") as fh:
                content = fh.read()
            file_fields.append(("screenshots", (os.path.basename(path), content, "application/octet-stream")))
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/results/environment/{environment_id}/instance/{similarity_id_2}/screenshots",
            files=file_fields,
        )
        return response.json().get("screenshot_ids", [])

    def delete_instance_screenshots(
        self, environment_id: str, similarity_id_2: str, screenshot_ids: List[str]
    ) -> bool:
        """DELETE .../instance/{similarity_id_2}/screenshots — delete
        screenshots for a DAST-detected instance.

        Args:
            environment_id (str): UUID of the Environment. Required.
            similarity_id_2 (str): The instance similarity ID (lowercase
                hex). Required.
            screenshot_ids (List[str]): IDs of the screenshots to
                delete. Required.

        Returns:
            bool: True if the API returned a 2xx status.
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=f"{self.base_url}/results/environment/{environment_id}/instance/{similarity_id_2}/screenshots",
            json={"screenshot_ids": screenshot_ids},
        )
        return 200 <= response.status_code < 300

    # ----- Pentest findings -----

    def get_pentest_findings(
        self, environment_id: str, pentest_scan_id: str
    ) -> List[DastPentestFindingResult]:
        """GET /results/environment/{environment_id}/pentest/{pentest_scan_id}/findings
        — get a pentest scan's findings.

        Args:
            environment_id (str): UUID of the Environment. Required.
            pentest_scan_id (str): UUID of the pentest scan. Required.

        Returns:
            List[DastPentestFindingResult]
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/pentest/{pentest_scan_id}/findings",
        )
        return [DastPentestFindingResult.from_dict(f) for f in (response.json() or [])]

    def get_pentest_finding_details(
        self, environment_id: str, pentest_scan_id: str, finding_id: str
    ) -> dict:
        """GET .../pentest/{pentest_scan_id}/findings/{finding_id} — get
        a pentest finding's steps and related DAST instances.

        Args:
            environment_id (str): UUID of the Environment. Required.
            pentest_scan_id (str): UUID of the pentest scan. Required.
            finding_id (str): The pentest finding ID. Required.

        Returns:
            dict: raw response body (PentestFindingDetails: steps,
            related_dast_instances) -- left unmodeled.
        """
        response = self.api_client.call_api(
            method="GET",
            url=(
                f"{self.base_url}/results/environment/{environment_id}"
                f"/pentest/{pentest_scan_id}/findings/{finding_id}"
            ),
        )
        return response.json()

    def get_pentest_wstg_coverage(
        self, environment_id: str, pentest_scan_id: str
    ) -> dict:
        """GET .../pentest/{pentest_scan_id}/wstg-coverage — get a
        pentest scan's OWASP WSTG test coverage.

        Args:
            environment_id (str): UUID of the Environment. Required.
            pentest_scan_id (str): UUID of the pentest scan. Required.

        Returns:
            dict: raw response body (PentestWstgCoverage: categories,
            tests) -- left unmodeled.
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/environment/{environment_id}/pentest/{pentest_scan_id}/wstg-coverage",
        )
        return response.json()


# ----- Module-level conveniences -----

def dast_get_results(
    scan_id: str,
    filter_: DastResultsFilter = None,
    page: int = None,
    per_page: int = None,
    search: str = None,
    sort_by: List[DastResultsSortBy] = None,
    group: str = None,
) -> DastResultsCollection:
    return DastResultsAPI().dast_get_results(
        scan_id=scan_id, filter_=filter_, page=page, per_page=per_page,
        search=search, sort_by=sort_by, group=group,
    )


def update_results(changelog: DastResultsChangelogInput) -> bool:
    return DastResultsAPI().update_results(changelog=changelog)


def get_result_info(result_id: str, scan_id: str) -> DastResultDetail:
    return DastResultsAPI().get_result_info(result_id=result_id, scan_id=scan_id)


def get_results_count_by_group(
    scan_id: str,
    group_by: List[DastResultsGroupBy] = None,
    filter_: DastResultsFilter = None,
    search: str = None,
) -> List[DastResultsGroupCount]:
    return DastResultsAPI().get_results_count_by_group(
        scan_id=scan_id, group_by=group_by, filter_=filter_, search=search,
    )
def health_check() -> str:
    return DastResultsAPI().health_check()


def get_alert_info(environment_id: str, scan_id: str, alert_id: str) -> DastAlertInfo:
    return DastResultsAPI().get_alert_info(environment_id=environment_id, scan_id=scan_id, alert_id=alert_id)


def get_alert_instances(environment_id: str, scan_id: str, alert_id: str, page: int, per_page: int, sort_by: List[str] = None, search: str = None, filter_: dict = None) -> DastAlertInstanceSummarizedList:
    return DastResultsAPI().get_alert_instances(environment_id=environment_id, scan_id=scan_id, alert_id=alert_id, page=page, per_page=per_page, sort_by=sort_by, search=search, filter_=filter_)


def get_alert_level_results(environment_id: str, scan_id: str, page: int, per_page: int, sort_by: List[str] = None, search: str = None, filter_: dict = None) -> DastAlertLevelResultList:
    return DastResultsAPI().get_alert_level_results(environment_id=environment_id, scan_id=scan_id, page=page, per_page=per_page, sort_by=sort_by, search=search, filter_=filter_)


def post_alert_level_results(environment_id: str, scan_id: str, body: dict = None) -> DastAlertLevelResultList:
    return DastResultsAPI().post_alert_level_results(environment_id=environment_id, scan_id=scan_id, body=body)


def get_grouped_alert_level_results(environment_id: str, scan_id: str, group: List[str], search: str = None, filter_: dict = None) -> List[DastGroups]:
    return DastResultsAPI().get_grouped_alert_level_results(environment_id=environment_id, scan_id=scan_id, group=group, search=search, filter_=filter_)


def post_grouped_alert_level_results(environment_id: str, scan_id: str, body: dict) -> List[DastGroups]:
    return DastResultsAPI().post_grouped_alert_level_results(environment_id=environment_id, scan_id=scan_id, body=body)


def get_full_scan_results(environment_id: str, scan_id: str) -> dict:
    return DastResultsAPI().get_full_scan_results(environment_id=environment_id, scan_id=scan_id)


def get_vulnerability_summary(environment_id: str, scan_id: str) -> DastVulnerabilitySummary:
    return DastResultsAPI().get_vulnerability_summary(environment_id=environment_id, scan_id=scan_id)


def is_alert_level_enabled() -> Optional[bool]:
    return DastResultsAPI().is_alert_level_enabled()


def get_aging_summary(scan_id: str) -> DastTimeSpanRiskSummary:
    return DastResultsAPI().get_aging_summary(scan_id=scan_id)


def get_instance_findings(scan_id: str, environment_id: str, similarity_id_2: str) -> dict:
    return DastResultsAPI().get_instance_findings(scan_id=scan_id, environment_id=environment_id, similarity_id_2=similarity_id_2)


def get_top_five_risks(scan_id: str, severity: str = None) -> List[DastTopFiveRisks]:
    return DastResultsAPI().get_top_five_risks(scan_id=scan_id, severity=severity)


def get_scan_sites_tree(environment_id: str, scan_id: str) -> List[dict]:
    return DastResultsAPI().get_scan_sites_tree(environment_id=environment_id, scan_id=scan_id)


def get_results_states_summary(app_id: str) -> Optional[DastResultsStatesSummary]:
    return DastResultsAPI().get_results_states_summary(app_id=app_id)


def get_compliance_analytics(app_id: str) -> Optional[DastComplianceAnalytics]:
    return DastResultsAPI().get_compliance_analytics(app_id=app_id)


def get_latest_correlation_results(environment_id: str, scan_id: str, similarity_id: str, type: str) -> dict:
    return DastResultsAPI().get_latest_correlation_results(environment_id=environment_id, scan_id=scan_id, similarity_id=similarity_id, type=type)


def get_compliance_over_time(environment_id: str, start_date: str, end_date: str, risk_levels: List[str] = None, compliance_types: List[str] = None) -> DastComplianceOverTimeResponse:
    return DastResultsAPI().get_compliance_over_time(environment_id=environment_id, start_date=start_date, end_date=end_date, risk_levels=risk_levels, compliance_types=compliance_types)


def get_occurrences_over_time(environment_id: str, scan_id: str = None, start: str = None, end: str = None, severity: List[str] = None, compliance: List[str] = None, include_manual_results: bool = None) -> DastAlertLevelOccurrencesResponse:
    return DastResultsAPI().get_occurrences_over_time(environment_id=environment_id, scan_id=scan_id, start=start, end=end, severity=severity, compliance=compliance, include_manual_results=include_manual_results)


def get_risk_level_over_time(environment_id: str, start_date: str, end_date: str, risk_levels: List[str] = None, compliance_types: List[str] = None) -> DastRiskLevelOverTimeResponse:
    return DastResultsAPI().get_risk_level_over_time(environment_id=environment_id, start_date=start_date, end_date=end_date, risk_levels=risk_levels, compliance_types=compliance_types)


def get_states_over_time(environment_id: str, start_date: str, end_date: str, risk_levels: List[str] = None, compliance_types: List[str] = None, include_manual_results: bool = None) -> DastStatesOverTimeResponse:
    return DastResultsAPI().get_states_over_time(environment_id=environment_id, start_date=start_date, end_date=end_date, risk_levels=risk_levels, compliance_types=compliance_types, include_manual_results=include_manual_results)


def get_manual_findings(environment_id: str, scan_id: str, alert_id: str = None, page: int = None, per_page: int = None, sort_by: List[str] = None, search: str = None, filter_: dict = None) -> DastManualFindingInstanceResultList:
    return DastResultsAPI().get_manual_findings(environment_id=environment_id, scan_id=scan_id, alert_id=alert_id, page=page, per_page=per_page, sort_by=sort_by, search=search, filter_=filter_)


def create_manual_findings_batch(environment_id: str, scan_id: str, findings: List[dict], only_current_scan: bool = None) -> str:
    return DastResultsAPI().create_manual_findings_batch(environment_id=environment_id, scan_id=scan_id, findings=findings, only_current_scan=only_current_scan)


def update_manual_finding_alert(environment_id: str, scan_id: str, update: dict) -> bool:
    return DastResultsAPI().update_manual_finding_alert(environment_id=environment_id, scan_id=scan_id, update=update)


def get_manual_finding_alert_info(environment_id: str, scan_id: str, alert_id: str) -> DastAlertInfo:
    return DastResultsAPI().get_manual_finding_alert_info(environment_id=environment_id, scan_id=scan_id, alert_id=alert_id)


def update_manual_finding_alert_instance(environment_id: str, scan_id: str, update: dict, screenshots: List[str] = None, delete_screenshot_ids: List[str] = None) -> bool:
    return DastResultsAPI().update_manual_finding_alert_instance(environment_id=environment_id, scan_id=scan_id, update=update, screenshots=screenshots, delete_screenshot_ids=delete_screenshot_ids)


def get_manual_findings_alert_level(environment_id: str, scan_id: str, page: int, per_page: int, sort_by: List[str] = None, search: str = None, filter_: dict = None) -> DastManualFindingsAlertLevelResultList:
    return DastResultsAPI().get_manual_findings_alert_level(environment_id=environment_id, scan_id=scan_id, page=page, per_page=per_page, sort_by=sort_by, search=search, filter_=filter_)


def get_grouped_manual_findings_alert_level(environment_id: str, scan_id: str, group: List[str], search: str = None, filter_: dict = None) -> List[DastGroups]:
    return DastResultsAPI().get_grouped_manual_findings_alert_level(environment_id=environment_id, scan_id=scan_id, group=group, search=search, filter_=filter_)


def delete_manual_finding_alerts(environment_id: str, scan_id: str, alert_ids: List[str]) -> bool:
    return DastResultsAPI().delete_manual_finding_alerts(environment_id=environment_id, scan_id=scan_id, alert_ids=alert_ids)


def get_grouped_manual_findings(environment_id: str, scan_id: str, group: List[str], search: str = None, filter_: dict = None) -> List[DastGroups]:
    return DastResultsAPI().get_grouped_manual_findings(environment_id=environment_id, scan_id=scan_id, group=group, search=search, filter_=filter_)


def update_manual_finding_instance(environment_id: str, scan_id: str, update: dict, screenshots: List[str] = None, delete_screenshot_ids: List[str] = None) -> bool:
    return DastResultsAPI().update_manual_finding_instance(environment_id=environment_id, scan_id=scan_id, update=update, screenshots=screenshots, delete_screenshot_ids=delete_screenshot_ids)


def get_manual_finding_instance_info(environment_id: str, scan_id: str, instance_id: str) -> DastResultDetail:
    return DastResultsAPI().get_manual_finding_instance_info(environment_id=environment_id, scan_id=scan_id, instance_id=instance_id)


def get_manual_finding_instance_screenshots(environment_id: str, scan_id: str, instance_id: str) -> List[DastScreenshot]:
    return DastResultsAPI().get_manual_finding_instance_screenshots(environment_id=environment_id, scan_id=scan_id, instance_id=instance_id)


def unlink_manual_findings(environment_id: str, scan_id: str, option: str) -> bool:
    return DastResultsAPI().unlink_manual_findings(environment_id=environment_id, scan_id=scan_id, option=option)


def delete_manual_finding_instances(environment_id: str, scan_id: str, alert_id: str, instance_ids: List[str]) -> bool:
    return DastResultsAPI().delete_manual_finding_instances(environment_id=environment_id, scan_id=scan_id, alert_id=alert_id, instance_ids=instance_ids)


def get_instance_screenshots(environment_id: str, similarity_id_2: str) -> List[DastScreenshot]:
    return DastResultsAPI().get_instance_screenshots(environment_id=environment_id, similarity_id_2=similarity_id_2)


def upload_instance_screenshots(environment_id: str, similarity_id_2: str, screenshots: List[str]) -> List[str]:
    return DastResultsAPI().upload_instance_screenshots(environment_id=environment_id, similarity_id_2=similarity_id_2, screenshots=screenshots)


def delete_instance_screenshots(environment_id: str, similarity_id_2: str, screenshot_ids: List[str]) -> bool:
    return DastResultsAPI().delete_instance_screenshots(environment_id=environment_id, similarity_id_2=similarity_id_2, screenshot_ids=screenshot_ids)


def get_pentest_findings(environment_id: str, pentest_scan_id: str) -> List[DastPentestFindingResult]:
    return DastResultsAPI().get_pentest_findings(environment_id=environment_id, pentest_scan_id=pentest_scan_id)


def get_pentest_finding_details(environment_id: str, pentest_scan_id: str, finding_id: str) -> dict:
    return DastResultsAPI().get_pentest_finding_details(environment_id=environment_id, pentest_scan_id=pentest_scan_id, finding_id=finding_id)


def get_pentest_wstg_coverage(environment_id: str, pentest_scan_id: str) -> dict:
    return DastResultsAPI().get_pentest_wstg_coverage(environment_id=environment_id, pentest_scan_id=pentest_scan_id)


