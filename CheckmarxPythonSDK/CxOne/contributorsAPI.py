from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    Contributors,
    ContributorInsights,
    ContributorUnfamiliarProjects,
)


class ContributorsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/contributors"
        )

    def get_allowed_and_current_contributors_for_the_current_tenant(
        self,
    ) -> Contributors:
        """
        Returns:
            Contributors
        """
        response = self.api_client.call_api(method="GET", url=self.base_url)
        return Contributors.from_dict(response.json())

    def get_contributors_details_for_current_tenant_exported_in_csv(
        self,
    ) -> bytes:
        """
        Returns:
            bytes (data of the csv file)
        """
        url = f"{self.base_url}/csv"
        response = self.api_client.call_api(method="GET", url=url)
        return response.content

    def get_contributor_insights_for_current_tenant(
        self,
    ) -> ContributorInsights:
        """
        Returns:
            ContributorInsights
        """
        url = f"{self.base_url}/insights"
        response = self.api_client.call_api(method="GET", url=url)
        return ContributorInsights.from_dict(response.json())

    def get_number_of_unfamiliar_projects(self) -> ContributorUnfamiliarProjects:
        """
        Get number of projects scanned in the last 90 days where
        contributors could not be counted.

        Returns:
            ContributorUnfamiliarProjects
        """
        url = f"{self.base_url}/unfamiliar_projects"
        response = self.api_client.call_api(method="GET", url=url)
        return ContributorUnfamiliarProjects.from_dict(response.json())

    def get_unfamiliar_projects_in_csv(self) -> bytes:
        """
        Returns:
            bytes (data of the csv file)
        """
        url = f"{self.base_url}/unfamiliar_projects/csv"
        response = self.api_client.call_api(method="GET", url=url)
        return response.content


def get_allowed_and_current_contributors_for_the_current_tenant() -> Contributors:
    return (
        ContributorsAPI().get_allowed_and_current_contributors_for_the_current_tenant()
    )


def get_contributors_details_for_current_tenant_exported_in_csv() -> bytes:
    return (
        ContributorsAPI().get_contributors_details_for_current_tenant_exported_in_csv()
    )


def get_contributor_insights_for_current_tenant() -> ContributorInsights:
    return ContributorsAPI().get_contributor_insights_for_current_tenant()


def get_number_of_unfamiliar_projects() -> ContributorUnfamiliarProjects:
    return ContributorsAPI().get_number_of_unfamiliar_projects()


def get_unfamiliar_projects_in_csv() -> bytes:
    return ContributorsAPI().get_unfamiliar_projects_in_csv()
