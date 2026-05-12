from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED, OK
from typing import List


class SastResultsPredicatesAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/sast-results-predicates"
        )

    def get_all_predicates_for_similarity_id(
        self,
        similarity_id: str,
        project_ids: List[str] = None,
        include_comment_json: bool = None,
        scan_id: str = None,
    ) -> dict:
        """
        Args:
            similarity_id (str):
            project_ids (list of str):
            include_comment_json (bool):
            scan_id (str):

        Returns:
            dict
        """
        url = f"{self.base_url}/{similarity_id}"
        params = {
            "project-ids": project_ids,
            "include-comment-json": include_comment_json,
            "scan-id": scan_id,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_latest_predicates_for_similarity_id(
        self,
        similarity_id: str,
        project_ids: List[str] = None,
        scan_id: str = None,
    ) -> dict:
        """
        Args:
            similarity_id (str):
            project_ids (list of str):
            scan_id (str):

        Returns:
            dict
        """
        url = f"{self.base_url}/{similarity_id}/latest"
        params = {"project-ids": project_ids, "scan-id": scan_id}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def predicate_severity_and_state_by_similarity_id_and_project_id(
        self, data: List[dict]
    ) -> bool:
        """
        Args:
            data (list of dict):

        Returns:
            bool
        """
        url = f"{self.base_url}/"
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        return response.status_code == CREATED

    def update_predicate_comment_by_predicate_id(
        self, data: List[dict]
    ) -> bool:
        """
        Args:
            data (list of dict):

        Returns:
            bool
        """
        url = f"{self.base_url}/"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=data
        )
        return response.status_code == NO_CONTENT

    def recalculate_summary_counters(self, data: dict) -> bool:
        """
        Args:
            data (dict):

        Returns:
            bool
        """
        url = f"{self.base_url}/recalculateSummaryCounters"
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        return response.status_code == OK

    def delete_a_predicate_history(
        self, similarity_id: str, project_id: str, predicate_id: str
    ) -> bool:
        """
        Args:
            similarity_id (str):
            project_id (str):
            predicate_id (str):

        Returns:
            bool
        """
        url = (
            f"{self.base_url}/{similarity_id}/{project_id}/{predicate_id}"
        )
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT


def get_all_predicates_for_similarity_id(
    similarity_id: str,
    project_ids: List[str] = None,
    include_comment_json: bool = None,
    scan_id: str = None,
) -> dict:
    return SastResultsPredicatesAPI().get_all_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        include_comment_json=include_comment_json,
        scan_id=scan_id,
    )


def get_latest_predicates_for_similarity_id(
    similarity_id: str,
    project_ids: List[str] = None,
    scan_id: str = None,
) -> dict:
    return SastResultsPredicatesAPI().get_latest_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        scan_id=scan_id,
    )


def predicate_severity_and_state_by_similarity_id_and_project_id(
    data: List[dict],
) -> bool:
    return SastResultsPredicatesAPI().predicate_severity_and_state_by_similarity_id_and_project_id(
        data=data
    )


def update_predicate_comment_by_predicate_id(data: List[dict]) -> bool:
    return SastResultsPredicatesAPI().update_predicate_comment_by_predicate_id(
        data=data
    )


def recalculate_summary_counters(data: dict) -> bool:
    return SastResultsPredicatesAPI().recalculate_summary_counters(data=data)


def delete_a_predicate_history(
    similarity_id: str, project_id: str, predicate_id: str
) -> bool:
    return SastResultsPredicatesAPI().delete_a_predicate_history(
        similarity_id=similarity_id,
        project_id=project_id,
        predicate_id=predicate_id,
    )
