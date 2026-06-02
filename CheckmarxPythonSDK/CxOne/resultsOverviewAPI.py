from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class ResultsOverviewAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/results-overview"
        )

    def get_projects_overview(
        self,
        project_ids: List[str],
        include_groups: bool = None,
        include_applications: bool = None,
        calculate_from_main_branch: bool = None,
    ) -> List[dict]:
        """
        Get overview for the tenant projects (deprecated).

        Args:
            project_ids (List[str]): List of project UUIDs (required)
            include_groups (bool): Include project groups
            include_applications (bool): Include project applications
            calculate_from_main_branch (bool): Use main branch only

        Returns:
            list of dict with project overview data
        """
        url = f"{self.base_url}/projects"
        params = {"projectIds": ",".join(project_ids)}
        if include_groups is not None:
            params["includeGroups"] = include_groups
        if include_applications is not None:
            params["includeApplications"] = include_applications
        if calculate_from_main_branch is not None:
            params["calculateFromMainBranch"] = calculate_from_main_branch
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


# ---- Module-level convenience function ----

def get_projects_overview(
    project_ids: List[str],
    include_groups: bool = None,
    include_applications: bool = None,
    calculate_from_main_branch: bool = None,
) -> List[dict]:
    return ResultsOverviewAPI().get_projects_overview(
        project_ids=project_ids,
        include_groups=include_groups,
        include_applications=include_applications,
        calculate_from_main_branch=calculate_from_main_branch,
    )
