from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import CREATED
from typing import List


class KicsResultsPredicatesAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/kics-results-predicates"
        )

    def get_predicates_by_similarity_id(
        self,
        similarity_id: str,
        project_ids: List[str] = None,
        scan_id: str = None,
    ) -> dict:
        """
        Get all predicates for a similarity ID.

        Args:
            similarity_id (str): Similarity ID
            project_ids (List[str]): Filter by project IDs (OR)
            scan_id (str): Scan ID

        Returns:
            dict with predicateHistoryPerProject and totalCount
        """
        url = f"{self.base_url}/{similarity_id}"
        params = {"project-ids": project_ids, "scan-id": scan_id}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_predicates_changes(
        self, similarity_id: str, project_id: str
    ) -> dict:
        """
        Get predicate changes for a similarity ID and project ID.

        Args:
            similarity_id (str): Similarity ID
            project_id (str): Project ID

        Returns:
            dict with projectId, similarityId, latestChanges,
            predicates, totalCount
        """
        url = (
            f"{self.base_url}/{similarity_id}"
            f"/projects/{project_id}"
        )
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def create_predicate(
        self, data: List[dict]
    ) -> bool:
        """
        Create predicates by similarity ID and project ID.

        Args:
            data (List[dict]): Each item requires similarityId, scanId,
                projectId. Optional: severity, state, comment, customStateId.
                state and customStateId cannot be used together.

        Returns:
            bool
        """
        url = f"{self.base_url}/"
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        return response.status_code == CREATED


# ---- Module-level convenience functions ----

def get_predicates_by_similarity_id(
    similarity_id: str,
    project_ids: List[str] = None,
    scan_id: str = None,
) -> dict:
    return KicsResultsPredicatesAPI().get_predicates_by_similarity_id(
        similarity_id=similarity_id, project_ids=project_ids, scan_id=scan_id,
    )


def get_predicates_changes(
    similarity_id: str, project_id: str
) -> dict:
    return KicsResultsPredicatesAPI().get_predicates_changes(
        similarity_id=similarity_id, project_id=project_id,
    )


def create_predicate(data: List[dict]) -> bool:
    return KicsResultsPredicatesAPI().create_predicate(data=data)
