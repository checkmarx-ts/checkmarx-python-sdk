from typing import List, Optional

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import RisksResponse


class RisksAPI(object):
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
    return RisksAPI().get_risks(
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
