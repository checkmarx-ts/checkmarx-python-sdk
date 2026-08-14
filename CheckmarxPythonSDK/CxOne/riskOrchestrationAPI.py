from typing import List, Optional

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import RisksAggregateResponse, RisksAiInsightsResponse, RisksResponse


class RiskOrchestrationAPI(object):
    """API client for the Risk Orchestration Service REST API.

    Provides access to aggregated project risks across all scanner engines.
    This endpoint does not return AI Triage & Remediation data; use
    GET /api/risks/ai-insights for risks with AI activity.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/risks"
        )

    def get_risks(
        self,
        project_id: str,
        asset_name: List[str] = None,
        asset_type: List[str] = None,
        engine: List[str] = None,
        from_date: str = None,
        limit: int = 20,
        offset: int = 0,
        order: str = "DESC",
        origin: List[str] = None,
        risk_name: List[str] = None,
        severity: List[str] = None,
        sort: str = None,
        source: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
        sub_asset_name: List[str] = None,
        to_date: str = None,
    ) -> RisksResponse:
        """Return a paginated list of risks for a project.

        This endpoint does not return AI Triage & Remediation data. To
        retrieve risks with AI insights use GET /api/risks/ai-insights.

        Args:
            project_id (str): Project UUID. Required.
            asset_name (List[str]): Filter by asset name (repeatable).
            asset_type (List[str]): Filter by asset type. Values: ENDPOINT,
                SOURCE_CODE, CONTAINER_IMAGE, MANIFEST_FILE, XML_FILE.
            engine (List[str]): Filter by engine. Values: SAST, IAC, SCA.
            from_date (str): Filter by first detection from date (inclusive).
                RFC3339 format, e.g. "2024-03-15T10:30:00+02:00".
            limit (int): Page size. 1–200. Default: 20.
            offset (int): Number of items to skip. Default: 0.
            order (str): Sort direction. ASC or DESC. Default: DESC.
            origin (List[str]): Filter by scan origin (repeatable).
            risk_name (List[str]): Filter by risk name (repeatable).
            severity (List[str]): Filter by severity. Values: CRITICAL,
                HIGH, MEDIUM, LOW, INFO.
            sort (str): Sort field. Values: severity, state, riskName,
                status, assetName, assetType, subAssetName, source,
                origin, firstDetectionDate.
            source (List[str]): Filter by source (repeatable).
            state (List[str]): Filter by state. Values: TO_VERIFY,
                NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT.
            status (List[str]): Filter by status. Values: NEW, RECURRENT,
                FIXED.
            sub_asset_name (List[str]): Filter by sub-asset name (repeatable).
            to_date (str): Filter by first detection to date (inclusive).
                RFC3339 format, e.g. "2024-03-15T10:30:00+02:00".

        Returns:
            RisksResponse: Pagination metadata and list of Risk objects.
        """
        params = {
            "projectId": project_id,
            "assetName": asset_name,
            "assetType": asset_type,
            "engine": engine,
            "fromDate": from_date,
            "limit": limit,
            "offset": offset,
            "order": order,
            "origin": origin,
            "riskName": risk_name,
            "severity": severity,
            "sort": sort,
            "source": source,
            "state": state,
            "status": status,
            "subAssetName": sub_asset_name,
            "toDate": to_date,
        }
        response = self.api_client.call_api(
            method="GET",
            url=self.base_url,
            params=params,
            headers={"Accept": "*/*; version=1.0"},
        )
        return RisksResponse.from_dict(response.json())

    def get_risks_ai_insights(
        self,
        project_id: str,
        ai_triage_completed_at_from: str = None,
        ai_triage_completed_at_to: str = None,
        ai_triage_exploitability: List[str] = None,
        ai_triage_fixability: List[str] = None,
        ai_triage_reachability: List[str] = None,
        ai_triage_status: List[str] = None,
        asset_name: List[str] = None,
        asset_type: List[str] = None,
        engine: List[str] = None,
        from_date: str = None,
        limit: int = 20,
        offset: int = 0,
        order: str = "DESC",
        origin: List[str] = None,
        remediation_status: List[str] = None,
        risk_name: List[str] = None,
        severity: List[str] = None,
        sort: str = None,
        source: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
        sub_asset_name: List[str] = None,
        to_date: str = None,
    ) -> RisksAiInsightsResponse:
        """Return risks with AI triage and remediation data for a project.

        Args:
            project_id (str): Project UUID. Required.
            ai_triage_completed_at_from (str): Filter by AI triage completion
                start date (inclusive). RFC3339 format.
            ai_triage_completed_at_to (str): Filter by AI triage completion
                end date (inclusive). RFC3339 format.
            ai_triage_exploitability (List[str]): Filter by exploitability.
                Values: UNKNOWN, EXPLOITABLE, NOT_EXPLOITABLE, UNDETERMINED.
            ai_triage_fixability (List[str]): Filter by fixability. Values:
                UNKNOWN, FIXABLE, NOT_FIXABLE.
            ai_triage_reachability (List[str]): Filter by reachability. Values:
                UNKNOWN, REACHABLE, NOT_REACHABLE, UNDETERMINED.
            ai_triage_status (List[str]): Filter by AI triage status. Values:
                TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE,
                CONFIRMED, URGENT.
            asset_name (List[str]): Filter by asset name (repeatable).
            asset_type (List[str]): Filter by asset type. Values: ENDPOINT,
                SOURCE_CODE, CONTAINER_IMAGE, MANIFEST_FILE, XML_FILE.
            engine (List[str]): Filter by engine. Values: SAST, IAC, SCA.
            from_date (str): Filter by first detection from date (inclusive).
                RFC3339 format.
            limit (int): Page size. 1–200. Default: 20.
            offset (int): Number of items to skip. Default: 0.
            order (str): Sort direction. ASC or DESC. Default: DESC.
            origin (List[str]): Filter by scan origin (repeatable).
            remediation_status (List[str]): Filter by remediation status.
                Values: NOT_STARTED, IN_PROGRESS, COMPLETED, FAILED.
            risk_name (List[str]): Filter by risk name (repeatable).
            severity (List[str]): Filter by severity. Values: CRITICAL,
                HIGH, MEDIUM, LOW, INFO.
            sort (str): Sort field. Values: severity, state, riskName, status,
                assetName, assetType, source, origin, firstDetectionDate,
                aiTriageStatus, aiTriageExploitability, aiTriageReachability,
                aiTriageFixability, aiTriageCompletedAt, remediationStatus,
                remediationCompletedAt.
            source (List[str]): Filter by source (repeatable).
            state (List[str]): Filter by state. Values: TO_VERIFY,
                NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT.
            status (List[str]): Filter by status. Values: NEW, RECURRENT,
                FIXED.
            sub_asset_name (List[str]): Filter by sub-asset name (repeatable).
            to_date (str): Filter by first detection to date (inclusive).
                RFC3339 format.

        Returns:
            RisksAiInsightsResponse: Pagination metadata and list of
                RiskWithAiInsights objects.
        """
        params = {
            "projectId": project_id,
            "aiTriageCompletedAtFrom": ai_triage_completed_at_from,
            "aiTriageCompletedAtTo": ai_triage_completed_at_to,
            "aiTriageExploitability": ai_triage_exploitability,
            "aiTriageFixability": ai_triage_fixability,
            "aiTriageReachability": ai_triage_reachability,
            "aiTriageStatus": ai_triage_status,
            "assetName": asset_name,
            "assetType": asset_type,
            "engine": engine,
            "fromDate": from_date,
            "limit": limit,
            "offset": offset,
            "order": order,
            "origin": origin,
            "remediationStatus": remediation_status,
            "riskName": risk_name,
            "severity": severity,
            "sort": sort,
            "source": source,
            "state": state,
            "status": status,
            "subAssetName": sub_asset_name,
            "toDate": to_date,
        }
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/ai-insights",
            params=params,
            headers={"Accept": "*/*; version=1.0"},
        )
        return RisksAiInsightsResponse.from_dict(response.json())

    def get_risks_aggregate(
        self,
        project_id: str,
        group_by: List[str],
        asset_name: List[str] = None,
        engine: List[str] = None,
        from_date: str = None,
        limit: int = 50,
        offset: int = 0,
        origin: List[str] = None,
        risk_name: List[str] = None,
        severity: List[str] = None,
        source: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
        to_date: str = None,
    ) -> RisksAggregateResponse:
        """Return aggregated risk counters for a project.

        Args:
            project_id (str): Project UUID. Required.
            group_by (List[str]): Grouping dimensions. Values: severity,
                engine. At least one required. Supply both for a per-engine
                per-severity breakdown.
            asset_name (List[str]): Filter by asset name (repeatable).
            engine (List[str]): Filter by engine. Values: SAST, IAC, SCA.
            from_date (str): Filter by first detection from date (inclusive).
                RFC3339 format.
            limit (int): Max results. 1–10000. Default: 50.
            offset (int): Results to skip. Default: 0.
            origin (List[str]): Filter by scan origin (repeatable).
            risk_name (List[str]): Filter by risk name (repeatable).
            severity (List[str]): Filter by severity. Values: CRITICAL,
                HIGH, MEDIUM, LOW, INFO.
            source (List[str]): Filter by source (repeatable).
            state (List[str]): Filter by state. Values: TO_VERIFY,
                NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT.
            status (List[str]): Filter by status. Values: NEW, RECURRENT,
                FIXED.
            to_date (str): Filter by first detection to date (inclusive).
                RFC3339 format.

        Returns:
            RisksAggregateResponse: List of RiskCounter objects.
        """
        params = {
            "groupBy": group_by,
            "projectId": project_id,
            "assetName": asset_name,
            "engine": engine,
            "fromDate": from_date,
            "limit": limit,
            "offset": offset,
            "origin": origin,
            "riskName": risk_name,
            "severity": severity,
            "source": source,
            "state": state,
            "status": status,
            "toDate": to_date,
        }
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/aggregate",
            params=params,
            headers={"Accept": "*/*; version=1.0"},
        )
        return RisksAggregateResponse.from_dict(response.json())


def get_risks(
    project_id: str,
    asset_name: List[str] = None,
    asset_type: List[str] = None,
    engine: List[str] = None,
    from_date: str = None,
    limit: int = 20,
    offset: int = 0,
    order: str = "DESC",
    origin: List[str] = None,
    risk_name: List[str] = None,
    severity: List[str] = None,
    sort: str = None,
    source: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
    sub_asset_name: List[str] = None,
    to_date: str = None,
) -> RisksResponse:
    """Return a paginated list of risks for a project.

    This endpoint does not return AI Triage & Remediation data. To retrieve
    risks with AI insights use GET /api/risks/ai-insights.

    Args:
        project_id (str): Project UUID. Required.
        asset_name (List[str]): Filter by asset name (repeatable).
        asset_type (List[str]): Filter by asset type. Values: ENDPOINT,
            SOURCE_CODE, CONTAINER_IMAGE, MANIFEST_FILE, XML_FILE.
        engine (List[str]): Filter by engine. Values: SAST, IAC, SCA.
        from_date (str): Filter by first detection from date (inclusive).
            RFC3339 format, e.g. "2024-03-15T10:30:00+02:00".
        limit (int): Page size. 1–200. Default: 20.
        offset (int): Number of items to skip. Default: 0.
        order (str): Sort direction. ASC or DESC. Default: DESC.
        origin (List[str]): Filter by scan origin (repeatable).
        risk_name (List[str]): Filter by risk name (repeatable).
        severity (List[str]): Filter by severity. Values: CRITICAL, HIGH,
            MEDIUM, LOW, INFO.
        sort (str): Sort field. Values: severity, state, riskName, status,
            assetName, assetType, subAssetName, source, origin,
            firstDetectionDate.
        source (List[str]): Filter by source (repeatable).
        state (List[str]): Filter by state. Values: TO_VERIFY,
            NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT.
        status (List[str]): Filter by status. Values: NEW, RECURRENT, FIXED.
        sub_asset_name (List[str]): Filter by sub-asset name (repeatable).
        to_date (str): Filter by first detection to date (inclusive).
            RFC3339 format, e.g. "2024-03-15T10:30:00+02:00".

    Returns:
        RisksResponse: Pagination metadata and list of Risk objects.
    """
    return RiskOrchestrationAPI().get_risks(
        project_id=project_id,
        asset_name=asset_name,
        asset_type=asset_type,
        engine=engine,
        from_date=from_date,
        limit=limit,
        offset=offset,
        order=order,
        origin=origin,
        risk_name=risk_name,
        severity=severity,
        sort=sort,
        source=source,
        state=state,
        status=status,
        sub_asset_name=sub_asset_name,
        to_date=to_date,
    )


def get_risks_ai_insights(
    project_id: str,
    ai_triage_completed_at_from: str = None,
    ai_triage_completed_at_to: str = None,
    ai_triage_exploitability: List[str] = None,
    ai_triage_fixability: List[str] = None,
    ai_triage_reachability: List[str] = None,
    ai_triage_status: List[str] = None,
    asset_name: List[str] = None,
    asset_type: List[str] = None,
    engine: List[str] = None,
    from_date: str = None,
    limit: int = 20,
    offset: int = 0,
    order: str = "DESC",
    origin: List[str] = None,
    remediation_status: List[str] = None,
    risk_name: List[str] = None,
    severity: List[str] = None,
    sort: str = None,
    source: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
    sub_asset_name: List[str] = None,
    to_date: str = None,
) -> RisksAiInsightsResponse:
    """Return risks with AI triage and remediation data for a project.

    Args:
        project_id (str): Project UUID. Required.
        ai_triage_completed_at_from (str): Filter by AI triage completion
            start date (inclusive). RFC3339 format.
        ai_triage_completed_at_to (str): Filter by AI triage completion
            end date (inclusive). RFC3339 format.
        ai_triage_exploitability (List[str]): Filter by exploitability.
            Values: UNKNOWN, EXPLOITABLE, NOT_EXPLOITABLE, UNDETERMINED.
        ai_triage_fixability (List[str]): Filter by fixability. Values:
            UNKNOWN, FIXABLE, NOT_FIXABLE.
        ai_triage_reachability (List[str]): Filter by reachability. Values:
            UNKNOWN, REACHABLE, NOT_REACHABLE, UNDETERMINED.
        ai_triage_status (List[str]): Filter by AI triage status. Values:
            TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED,
            URGENT.
        asset_name (List[str]): Filter by asset name (repeatable).
        asset_type (List[str]): Filter by asset type. Values: ENDPOINT,
            SOURCE_CODE, CONTAINER_IMAGE, MANIFEST_FILE, XML_FILE.
        engine (List[str]): Filter by engine. Values: SAST, IAC, SCA.
        from_date (str): Filter by first detection from date (inclusive).
            RFC3339 format.
        limit (int): Page size. 1–200. Default: 20.
        offset (int): Number of items to skip. Default: 0.
        order (str): Sort direction. ASC or DESC. Default: DESC.
        origin (List[str]): Filter by scan origin (repeatable).
        remediation_status (List[str]): Filter by remediation status.
            Values: NOT_STARTED, IN_PROGRESS, COMPLETED, FAILED.
        risk_name (List[str]): Filter by risk name (repeatable).
        severity (List[str]): Filter by severity. Values: CRITICAL, HIGH,
            MEDIUM, LOW, INFO.
        sort (str): Sort field. Values: severity, state, riskName, status,
            assetName, assetType, source, origin, firstDetectionDate,
            aiTriageStatus, aiTriageExploitability, aiTriageReachability,
            aiTriageFixability, aiTriageCompletedAt, remediationStatus,
            remediationCompletedAt.
        source (List[str]): Filter by source (repeatable).
        state (List[str]): Filter by state. Values: TO_VERIFY,
            NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT.
        status (List[str]): Filter by status. Values: NEW, RECURRENT, FIXED.
        sub_asset_name (List[str]): Filter by sub-asset name (repeatable).
        to_date (str): Filter by first detection to date (inclusive).
            RFC3339 format.

    Returns:
        RisksAiInsightsResponse: Pagination metadata and list of
            RiskWithAiInsights objects.
    """
    return RiskOrchestrationAPI().get_risks_ai_insights(
        project_id=project_id,
        ai_triage_completed_at_from=ai_triage_completed_at_from,
        ai_triage_completed_at_to=ai_triage_completed_at_to,
        ai_triage_exploitability=ai_triage_exploitability,
        ai_triage_fixability=ai_triage_fixability,
        ai_triage_reachability=ai_triage_reachability,
        ai_triage_status=ai_triage_status,
        asset_name=asset_name,
        asset_type=asset_type,
        engine=engine,
        from_date=from_date,
        limit=limit,
        offset=offset,
        order=order,
        origin=origin,
        remediation_status=remediation_status,
        risk_name=risk_name,
        severity=severity,
        sort=sort,
        source=source,
        state=state,
        status=status,
        sub_asset_name=sub_asset_name,
        to_date=to_date,
    )


def get_risks_aggregate(
    project_id: str,
    group_by: List[str],
    asset_name: List[str] = None,
    engine: List[str] = None,
    from_date: str = None,
    limit: int = 50,
    offset: int = 0,
    origin: List[str] = None,
    risk_name: List[str] = None,
    severity: List[str] = None,
    source: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
    to_date: str = None,
) -> RisksAggregateResponse:
    """Return aggregated risk counters for a project.

    Args:
        project_id (str): Project UUID. Required.
        group_by (List[str]): Grouping dimensions. Values: severity, engine.
            At least one required. Supply both for a per-engine per-severity
            breakdown.
        asset_name (List[str]): Filter by asset name (repeatable).
        engine (List[str]): Filter by engine. Values: SAST, IAC, SCA.
        from_date (str): Filter by first detection from date (inclusive).
            RFC3339 format.
        limit (int): Max results. 1–10000. Default: 50.
        offset (int): Results to skip. Default: 0.
        origin (List[str]): Filter by scan origin (repeatable).
        risk_name (List[str]): Filter by risk name (repeatable).
        severity (List[str]): Filter by severity. Values: CRITICAL, HIGH,
            MEDIUM, LOW, INFO.
        source (List[str]): Filter by source (repeatable).
        state (List[str]): Filter by state. Values: TO_VERIFY,
            NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT.
        status (List[str]): Filter by status. Values: NEW, RECURRENT, FIXED.
        to_date (str): Filter by first detection to date (inclusive).
            RFC3339 format.

    Returns:
        RisksAggregateResponse: List of RiskCounter objects.
    """
    return RiskOrchestrationAPI().get_risks_aggregate(
        project_id=project_id,
        group_by=group_by,
        asset_name=asset_name,
        engine=engine,
        from_date=from_date,
        limit=limit,
        offset=offset,
        origin=origin,
        risk_name=risk_name,
        severity=severity,
        source=source,
        state=state,
        status=status,
        to_date=to_date,
    )
