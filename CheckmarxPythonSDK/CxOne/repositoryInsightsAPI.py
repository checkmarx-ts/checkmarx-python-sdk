from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class RepositoryInsightsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/insights"
        )

    def get_project_repositories(
        self,
        project_id: str,
        offset: int = 0,
        limit: int = 25,
    ) -> dict:
        """
        Get a list of repositories by project.

        Args:
            project_id (str): Project ID
            offset (int): Items to skip. Default: 0
            limit (int): Max results (1-200). Default: 25

        Returns:
            dict with project_id, project_name, last_scan_date,
            total_loc, total_scanned_files, total_unscanned_files,
            total_repositories, page, repositories
        """
        url = f"{self.base_url}/project/{project_id}"
        params = {"offset": offset, "limit": limit}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_insights_by_repository(self, repository_url: str) -> dict:
        """
        Get insights by repository URL.

        Args:
            repository_url (str): Repository URL

        Returns:
            dict with lastScanDate, repositoryURL, scanID, insights
            (containing SAST, KICS, and RecentCommits sub-objects)
        """
        url = f"{self.base_url}/repository"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json={"repository_url": repository_url},
        )
        return response.json()


# ---- Module-level convenience functions ----

def get_project_repositories(
    project_id: str,
    offset: int = 0,
    limit: int = 25,
) -> dict:
    return RepositoryInsightsAPI().get_project_repositories(
        project_id=project_id, offset=offset, limit=limit,
    )


def get_insights_by_repository(repository_url: str) -> dict:
    return RepositoryInsightsAPI().get_insights_by_repository(
        repository_url=repository_url
    )
