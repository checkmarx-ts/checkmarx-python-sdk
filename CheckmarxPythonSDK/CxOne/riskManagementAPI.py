from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from typing import List


class RiskManagementAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/risk-management"
        )

    def get_summary(self) -> dict:
        """
        Get risk management summary for all applications.

        Returns:
            dict with applications array
        """
        url = f"{self.base_url}/summary"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_results(
        self,
        application_id: str,
        sort: str = None,
        type: List[str] = None,
        vulnerability_name: List[str] = None,
        project_criticality: List[str] = None,
        runtime: bool = None,
        origin: List[str] = None,
        risk_score: List[str] = None,
        created_at: List[str] = None,
        additional_trait: List[str] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> dict:
        """
        List results by application.

        Args:
            application_id (str): Application ID (uuid)
            sort (str): Sort field. Default: -risk-score
            type (List[str]): Filter by: framework, infra, byor
            vulnerability_name (List[str]): CSV of vulnerability names
            project_criticality (List[str]): CSV of criticality values
            runtime (bool): Filter by runtime status
            origin (List[str]): CSV of origin strings
            risk_score (List[str]): CSV of scores/ranges (0.0-10.0)
            created_at (List[str]): CSV of day ranges
            additional_trait (List[str]): exploitable_path, suspected_malware,
                neither
            offset (int): Pagination offset. Default: 0
            limit (int): Page size (max 1000). Default: 10

        Returns:
            dict with results, totalCount, application, search, filters, sorts
        """
        url = f"{self.base_url}/{application_id}/results"
        params = {
            "sort": sort,
            "type": type,
            "vulnerability-name": vulnerability_name,
            "project-criticality": project_criticality,
            "runtime": runtime,
            "origin": origin,
            "risk-score": risk_score,
            "created-at": created_at,
            "additional-trait": additional_trait,
            "offset": offset,
            "limit": limit,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_score_card(self, id: str) -> dict:
        """
        Get score card information for a result.

        Args:
            id (str): Result ID (uuid)

        Returns:
            dict — discriminated union: SastScoreCard, ScaScoreCard,
            KicsScoreCard, or ByorScoreCard
        """
        url = f"{self.base_url}/result/{id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def update_result_state(
        self, application_id: str, id: str, state: str
    ) -> bool:
        """
        Update a result's state.

        Args:
            application_id (str): Application ID (uuid)
            id (str): Result ID (uuid)
            state (str): new, processing, or analyzed

        Returns:
            bool
        """
        url = f"{self.base_url}/{application_id}/results/{id}"
        response = self.api_client.call_api(
            method="PUT", url=url, json={"state": state}
        )
        return response.status_code == NO_CONTENT

    def update_assignees(self, results: List[dict]) -> dict:
        """
        Update assignees for multiple results.

        Args:
            results (List[dict]): Each item with resultId (required),
                applicationId (required), and optional usersToAdd,
                usersToRemove, groupsToAdd, groupsToRemove.

        Returns:
            dict with response array (per-result success/errors)
        """
        url = f"{self.base_url}/updateAssignees"
        response = self.api_client.call_api(
            method="PUT", url=url, json={"results": results}
        )
        return response.json()


# ---- Module-level convenience functions ----

def get_summary() -> dict:
    return RiskManagementAPI().get_summary()


def get_results(
    application_id: str,
    sort: str = None,
    type: List[str] = None,
    vulnerability_name: List[str] = None,
    project_criticality: List[str] = None,
    runtime: bool = None,
    origin: List[str] = None,
    risk_score: List[str] = None,
    created_at: List[str] = None,
    additional_trait: List[str] = None,
    offset: int = 0,
    limit: int = 10,
) -> dict:
    return RiskManagementAPI().get_results(
        application_id=application_id, sort=sort, type=type,
        vulnerability_name=vulnerability_name,
        project_criticality=project_criticality, runtime=runtime,
        origin=origin, risk_score=risk_score, created_at=created_at,
        additional_trait=additional_trait, offset=offset, limit=limit,
    )


def get_score_card(id: str) -> dict:
    return RiskManagementAPI().get_score_card(id=id)


def update_result_state(
    application_id: str, id: str, state: str
) -> bool:
    return RiskManagementAPI().update_result_state(
        application_id=application_id, id=id, state=state
    )


def update_assignees(results: List[dict]) -> dict:
    return RiskManagementAPI().update_assignees(results=results)
