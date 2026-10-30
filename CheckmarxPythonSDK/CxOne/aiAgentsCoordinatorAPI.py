from typing import List, Optional, Union

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    AiCoordinatorAccountConfigResponse,
    AiCoordinatorAutoTriageAccountConfigWriteItem,
    AiCoordinatorAutoRemediationAccountConfigWriteItem,
    AiCoordinatorProjectConfigResponse,
    AiCoordinatorAutoTriageProjectConfigWriteItem,
    AiCoordinatorAutoRemediationProjectConfigWriteItem,
    AiCoordinatorHistoryListResponse,
    AiCoordinatorHistoryFieldValuesResponse,
)


class AiAgentsCoordinatorAPI(object):
    """API client for the AI Agents Coordinator REST API.

    Retrieves and manages AI Triage and AI Remediation configurations at
    the account and project levels: enable/disable automatic triage and
    remediation, define which findings are eligible for processing, and
    control which settings projects may override. Also exposes the
    execution history (and CSV export) of automated triage/remediation
    actions. Currently supported for the SAST and SCA scanners.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/ai-agents-coordinator"
        )

    # ----- Configuration -----

    def get_account_configuration(self) -> AiCoordinatorAccountConfigResponse:
        """GET /configuration — get the account-level auto-triage/
        auto-remediation configuration.

        Returns:
            AiCoordinatorAccountConfigResponse
        """
        response = self.api_client.call_api(method="GET", url=f"{self.base_url}/configuration")
        return AiCoordinatorAccountConfigResponse.from_dict(response.json())

    def update_account_configuration(
        self,
        configurations: List[
            Union[
                AiCoordinatorAutoTriageAccountConfigWriteItem,
                AiCoordinatorAutoRemediationAccountConfigWriteItem,
            ]
        ],
    ) -> AiCoordinatorAccountConfigResponse:
        """PUT /configuration — upsert the account-level auto-triage/
        auto-remediation configuration.

        Args:
            configurations (List[AiCoordinatorAutoTriageAccountConfigWriteItem |
                AiCoordinatorAutoRemediationAccountConfigWriteItem]): 1-2
                entries, at most one per feature (auto_triage,
                auto_remediation). Required.

        Returns:
            AiCoordinatorAccountConfigResponse
        """
        body = {"configurations": [c.to_dict() for c in configurations]}
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/configuration", json=body,
        )
        return AiCoordinatorAccountConfigResponse.from_dict(response.json())

    def get_project_configuration(self, project_id: str) -> AiCoordinatorProjectConfigResponse:
        """GET /projects/{project_id}/configuration — get a project's
        auto-triage/auto-remediation configuration.

        Args:
            project_id (str): UUID of the Checkmarx One project. Required.

        Returns:
            AiCoordinatorProjectConfigResponse
        """
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/projects/{project_id}/configuration",
        )
        return AiCoordinatorProjectConfigResponse.from_dict(response.json())

    def update_project_configuration(
        self,
        project_id: str,
        configurations: List[
            Union[
                AiCoordinatorAutoTriageProjectConfigWriteItem,
                AiCoordinatorAutoRemediationProjectConfigWriteItem,
            ]
        ],
    ) -> AiCoordinatorProjectConfigResponse:
        """PUT /projects/{project_id}/configuration — upsert a project's
        auto-triage/auto-remediation configuration, provided the account
        configuration's allowOverride permits the relevant overrides.

        Args:
            project_id (str): UUID of the Checkmarx One project. Required.
            configurations (List[AiCoordinatorAutoTriageProjectConfigWriteItem |
                AiCoordinatorAutoRemediationProjectConfigWriteItem]): 1-2
                entries, at most one per feature. Required.

        Returns:
            AiCoordinatorProjectConfigResponse
        """
        body = {"configurations": [c.to_dict() for c in configurations]}
        response = self.api_client.call_api(
            method="PUT", url=f"{self.base_url}/projects/{project_id}/configuration",
            json=body,
        )
        return AiCoordinatorProjectConfigResponse.from_dict(response.json())

    # ----- History -----

    def list_history(
        self,
        limit: int = 50,
        offset: int = 0,
        project_name: str = None,
        project_names: List[str] = None,
        origins: List[str] = None,
        scanners: List[str] = None,
        from_date: str = None,
        to_date: str = None,
        sort: str = "completedAt",
        order: str = "DESC",
    ) -> AiCoordinatorHistoryListResponse:
        """GET /history — list auto-action (auto-triage/auto-remediation)
        execution history, paginated/filtered/sorted.

        Args:
            limit (int, optional): Page size, 1-200. Defaults to 50.
            offset (int, optional): Pagination offset. Defaults to 0.
            project_name (str, optional): Filter by a single project name.
            project_names (List[str], optional): Filter by multiple
                project names (sent as a comma-separated string).
            origins (List[str], optional): Filter by origin (sent as a
                comma-separated string).
            scanners (List[str], optional): Filter by scanner type, e.g.
                ["SAST", "SCA"] (sent as a comma-separated string).
            from_date (str, optional): Start of the date range (RFC3339).
            to_date (str, optional): End of the date range (RFC3339).
            sort (str, optional): v1 only supports "completedAt".
                Defaults to "completedAt".
            order (str, optional): "ASC" or "DESC". Defaults to "DESC".

        Returns:
            AiCoordinatorHistoryListResponse
        """
        params = {
            "limit": limit,
            "offset": offset,
            "projectName": project_name,
            "projectNames": ",".join(project_names) if project_names else None,
            "origins": ",".join(origins) if origins else None,
            "scanners": ",".join(scanners) if scanners else None,
            "fromDate": from_date,
            "toDate": to_date,
            "sort": sort,
            "order": order,
        }
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/history", params=params,
        )
        return AiCoordinatorHistoryListResponse.from_dict(response.json())

    def list_history_field_values(
        self,
        field: str,
        search: str = None,
        limit: int = 50,
        offset: int = 0,
    ) -> AiCoordinatorHistoryFieldValuesResponse:
        """GET /history/fieldValues — list distinct filter values for a
        History Tab column (v1 supports only field="projectNames").

        Args:
            field (str): The column to list distinct values for. v1 only
                supports "projectNames". Required.
            search (str, optional): Case-insensitive substring match on
                the filter values.
            limit (int, optional): Page size, 1-200. Defaults to 50.
            offset (int, optional): Pagination offset. Defaults to 0.

        Returns:
            AiCoordinatorHistoryFieldValuesResponse
        """
        params = {"field": field, "search": search, "limit": limit, "offset": offset}
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/history/fieldValues", params=params,
        )
        return AiCoordinatorHistoryFieldValuesResponse.from_dict(response.json())

    def export_history_csv(
        self,
        project_name: str = None,
        project_names: List[str] = None,
        origins: List[str] = None,
        scanners: List[str] = None,
        from_date: str = None,
        to_date: str = None,
        sort: str = "completedAt",
        order: str = "DESC",
    ) -> str:
        """GET /history/export/csv — export auto-action execution history
        as CSV, with the same filters as list_history (no pagination --
        the whole filtered result set is exported).

        The spec declares the response content type as application/json
        with an empty schema, but "export ... as CSV" strongly implies a
        text/csv body; this returns response.text rather than
        response.json() to be safe either way.

        Args:
            project_name (str, optional): Filter by a single project name.
            project_names (List[str], optional): Filter by multiple
                project names (sent as a comma-separated string).
            origins (List[str], optional): Filter by origin (sent as a
                comma-separated string).
            scanners (List[str], optional): Filter by scanner type (sent
                as a comma-separated string).
            from_date (str, optional): Start of the date range (RFC3339).
            to_date (str, optional): End of the date range (RFC3339).
            sort (str, optional): v1 only supports "completedAt".
                Defaults to "completedAt".
            order (str, optional): "ASC" or "DESC". Defaults to "DESC".

        Returns:
            str: the CSV (or JSON, depending on tenant) response body.
        """
        params = {
            "projectName": project_name,
            "projectNames": ",".join(project_names) if project_names else None,
            "origins": ",".join(origins) if origins else None,
            "scanners": ",".join(scanners) if scanners else None,
            "fromDate": from_date,
            "toDate": to_date,
            "sort": sort,
            "order": order,
        }
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/history/export/csv", params=params,
        )
        return response.text


def get_account_configuration() -> AiCoordinatorAccountConfigResponse:
    return AiAgentsCoordinatorAPI().get_account_configuration()


def update_account_configuration(
    configurations: List[
        Union[
            AiCoordinatorAutoTriageAccountConfigWriteItem,
            AiCoordinatorAutoRemediationAccountConfigWriteItem,
        ]
    ],
) -> AiCoordinatorAccountConfigResponse:
    return AiAgentsCoordinatorAPI().update_account_configuration(configurations=configurations)


def get_project_configuration(project_id: str) -> AiCoordinatorProjectConfigResponse:
    return AiAgentsCoordinatorAPI().get_project_configuration(project_id=project_id)


def update_project_configuration(
    project_id: str,
    configurations: List[
        Union[
            AiCoordinatorAutoTriageProjectConfigWriteItem,
            AiCoordinatorAutoRemediationProjectConfigWriteItem,
        ]
    ],
) -> AiCoordinatorProjectConfigResponse:
    return AiAgentsCoordinatorAPI().update_project_configuration(
        project_id=project_id, configurations=configurations,
    )


def list_history(
    limit: int = 50,
    offset: int = 0,
    project_name: str = None,
    project_names: List[str] = None,
    origins: List[str] = None,
    scanners: List[str] = None,
    from_date: str = None,
    to_date: str = None,
    sort: str = "completedAt",
    order: str = "DESC",
) -> AiCoordinatorHistoryListResponse:
    return AiAgentsCoordinatorAPI().list_history(
        limit=limit, offset=offset, project_name=project_name,
        project_names=project_names, origins=origins, scanners=scanners,
        from_date=from_date, to_date=to_date, sort=sort, order=order,
    )


def list_history_field_values(
    field: str, search: str = None, limit: int = 50, offset: int = 0,
) -> AiCoordinatorHistoryFieldValuesResponse:
    return AiAgentsCoordinatorAPI().list_history_field_values(
        field=field, search=search, limit=limit, offset=offset,
    )


def export_history_csv(
    project_name: str = None,
    project_names: List[str] = None,
    origins: List[str] = None,
    scanners: List[str] = None,
    from_date: str = None,
    to_date: str = None,
    sort: str = "completedAt",
    order: str = "DESC",
) -> str:
    return AiAgentsCoordinatorAPI().export_history_csv(
        project_name=project_name, project_names=project_names, origins=origins,
        scanners=scanners, from_date=from_date, to_date=to_date, sort=sort, order=order,
    )
