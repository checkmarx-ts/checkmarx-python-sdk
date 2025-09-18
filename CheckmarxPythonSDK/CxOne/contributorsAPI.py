from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    Contributors, construct_contributors,
    ContributorInsights, construct_contributor_insights,
    ContributorUnfamiliarProjects, construct_contributor_unfamiliar_projects,

)

api_url = "/api/contributors"


class ContributorsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_allowed_and_current_contributors_for_the_current_tenant(self) -> Contributors:
        """

        Returns:

        """
        relative_url = api_url
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_contributors(item)

    def get_contributors_details_for_current_tenant_exported_in_csv(self) -> bytes:
        """

        Returns:
            bytes (data of the csv file)
        """
        relative_url = api_url + "/csv"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.content

    def get_contributor_insights_for_current_tenant(self) -> ContributorInsights:
        relative_url = api_url + "/insights"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_contributor_insights(item)

    def get_number_of_unfamiliar_projects(self) -> ContributorUnfamiliarProjects:
        """get number of projects scanned in the last 90 days where contributors couldn't be counted"""
        relative_url = api_url + "/unfamiliar_projects"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_contributor_unfamiliar_projects(item)

    def get_unfamiliar_projects_in_csv(self) -> bytes:
        relative_url = api_url + "/unfamiliar_projects/csv"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.content


def get_allowed_and_current_contributors_for_the_current_tenant() -> Contributors:
    return ContributorsAPI().get_allowed_and_current_contributors_for_the_current_tenant()


def get_contributors_details_for_current_tenant_exported_in_csv() -> bytes:
    return ContributorsAPI().get_contributors_details_for_current_tenant_exported_in_csv()


def get_contributor_insights_for_current_tenant() -> ContributorInsights:
    return ContributorsAPI().get_contributor_insights_for_current_tenant()


def get_number_of_unfamiliar_projects() -> ContributorUnfamiliarProjects:
    return ContributorsAPI().get_number_of_unfamiliar_projects()


def get_unfamiliar_projects_in_csv() -> bytes:
    return ContributorsAPI().get_unfamiliar_projects_in_csv()
