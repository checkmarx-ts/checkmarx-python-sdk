from CheckmarxPythonSDK.api_client import ApiClient
from typing import List
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import OK
from .utilities import type_check
from .dto import (
    CloudInsightCreateEnrichAccount,
    CloudInsightEnrichAccount, construct_cloud_insight_enrich_account,
    CloudInsightAccount, construct_cloud_insight_account,
    StartEnrich,
    PaginatedAccountLogsListResponse, construct_paginated_account_logs_list_response,
    PaginatedAccountsListResponse, construct_paginated_accounts_list_response,
    PaginatedContainersListResponse, construct_paginated_containers_list_response,
    PaginatedResourcesList, construct_paginated_resources_list,
)

api_url = "/api/cnas"


class CloudInsightsServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_enrich_account(self, data: CloudInsightCreateEnrichAccount) -> CloudInsightEnrichAccount:
        """

        Args:
            data (CloudInsightCreateEnrichAccount):

        Returns:
            CloudInsightEnrichAccount
        """
        type_check(data, CloudInsightCreateEnrichAccount)
        relative_url = api_url + "/accounts/enrich"
        response = self.api_client.post_request(relative_url=relative_url, json=data.to_dict())
        return construct_cloud_insight_enrich_account(response.json())

    def get_enrich_account_by_external_id(
            self, external_id: str, offset: int = 0, limit: int = 100
    ) -> PaginatedAccountsListResponse:
        """

        Args:
            external_id (str): A unique identifier provided by Checkmarx
            offset (int): Offset the results Default value : 0
            limit (int): Limit the number of results

        Returns:
            PaginatedAccountsListResponse
        """
        type_check(external_id, str)
        type_check(offset, int)
        type_check(limit, int)
        params = {"external-id": external_id, "offset": offset, "limit": limit}
        relative_url = api_url + "/accounts/enrich"
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_paginated_accounts_list_response(response.json())

    def start_enrichment(self, cloud_insights_account_id: str, start_enrich: StartEnrich) -> str:
        """

        Args:
            cloud_insights_account_id (str):   uuid4
            start_enrich (StartEnrich)

        Returns:
            message (str)
        """
        type_check(cloud_insights_account_id, str)
        type_check(start_enrich, StartEnrich)
        relative_url = api_url + "/accounts/{id}/enrich".format(id=cloud_insights_account_id)
        response = self.api_client.post_request(relative_url=relative_url, json=start_enrich.to_dict())
        return response.json().get("message")

    def start_async_enrichment(self, cloud_insights_account_id: str, start_enrich: StartEnrich) -> str:
        relative_url = api_url + "/v2/accounts/{id}/enrich".format(id=cloud_insights_account_id)
        response = self.api_client.post_request(relative_url=relative_url, json=start_enrich.to_dict())
        return response.json().get("syncId")

    def get_cloud_insight_account(self, account_id: str) -> CloudInsightAccount:
        """

        Args:
            account_id (str): Cloud Insights account ID

        Returns:
            CloudInsightAccount
        """
        type_check(account_id, str)
        relative_url = api_url + "/accounts/{id}".format(id=account_id)
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_cloud_insight_account(response.json())

    def delete_cloud_insight_account(self, account_id: str) -> bool:
        """

          Args:
              account_id (str): Cloud Insights account ID

          Returns:
              bool
          """
        relative_url = api_url + "/accounts/{id}".format(id=account_id)
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == OK

    def get_account_logs(
            self, account_id: str, event_type: str, status: str, description: str, created_at_start: str,
            created_at_end: str,
    ) -> PaginatedAccountLogsListResponse:
        """

        Args:
            account_id (str): Cloud Insights account ID
            event_type (str): Available values : Incoming, Outgoing
            status (str):  Available values : Success, Failed
            description (str):  Available values : Sync, Scheduled
            created_at_start (str): Start of the creation date range in ISO 8601 format (e.g., 2025-08-10T00:00:00Z).
            created_at_end (str): End of the creation date range in ISO 8601 format (e.g., 2025-08-12T23:59:59Z).

        Returns:
            PaginatedAccountLogsListResponse
        """
        relative_url = api_url + "/accounts/{id}/logs".format(id=account_id)
        params = {
            "eventType": event_type, "status": status, "description": description,
            "createdAtStart": created_at_start, "createdAtEnd": created_at_end
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_paginated_account_logs_list_response(response.json())

    def get_all_containers_for_an_account_id(
            self, account_id: str, limit: int = 100, offset: int = 0, image_name: str = None,
            image_short_name: str = None, project_name: str = None, repo_url: str = None, cluster_name: str = None,
            public_exposed: str = None, search: str = None, cluster_id: str = None, order_column: str = None,
            order_direction: str = None
    ) -> PaginatedContainersListResponse:
        """

        Args:
            account_id (str): Cloud Insights account ID
            limit (int): Limit the number of results
            offset (int): Offset the results Default value : 0
            image_name (str):
            image_short_name (str):
            project_name (str):
            repo_url (str):
            cluster_name (str):
            public_exposed (str):
            search (str):
            cluster_id (str):
            order_column (str):
            order_direction (str):

        Returns:
            PaginatedContainersListResponse
        """
        type_check(account_id, str)
        type_check(limit, int)
        type_check(offset, int)
        type_check(image_name, str)
        type_check(image_short_name, str)
        type_check(project_name, str)
        type_check(repo_url, str)
        type_check(cluster_name, str)
        type_check(public_exposed, str)
        type_check(search, str)
        type_check(cluster_id, str)
        type_check(order_column, str)
        type_check(order_direction, str)
        relative_url = api_url + f"/accounts/{account_id}/containers"
        params = {
            "limit": limit, "offset": offset, "image-name": image_name, "image-short-name": image_short_name,
            "project-name": project_name, "repo-url": repo_url, "cluster-name": cluster_name,
            "public-exposed": public_exposed, "search": search, "cluster-id": cluster_id,
            "order-column": order_column, "order-direction": order_direction,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_paginated_containers_list_response(response.json())

    def get_resources_filtered_by_group(
            self, account_id: str, image_name: str = None, image_short_name: str = None, public_exposed: str = None,
            search: str = None, cluster_names: List[str] = None, asset_types: List[str] = None,
            resource_type: str = None, offset: int = 0, limit: int = 100, order_column: str = None,
            order_direction: str = None,
    ) -> PaginatedResourcesList:
        """

        Args:
            account_id (str):
            image_name (str):
            image_short_name (str):
            public_exposed (str):
            search (str):
            cluster_names (List[str]):  Filter by cluster names (comma-separated)
            asset_types (List[str]): Filter by asset types (comma-separated) Available values : ECS, Kubernetes
            resource_type (str): Available values : CONTAINER
            offset (int):
            limit (int):
            order_column (str):
            order_direction (str):

        Returns:

        """
        relative_url = api_url + f"/accounts/{account_id}/resources"
        params = {
            "image-name": image_name, "image-short-name": image_short_name, "public-exposed": public_exposed,
            "search": search, "cluster-name": ",".join(cluster_names) if cluster_names else None,
            "asset-type": ",".join(asset_types) if asset_types else None,
            "resource-type": resource_type,
            "offset": offset, "limit": limit, "order-column": order_column, "order-direction": order_direction,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_paginated_resources_list(response.json())


def create_enrich_account(data: CloudInsightCreateEnrichAccount) -> CloudInsightEnrichAccount:
    return CloudInsightsServiceAPI().create_enrich_account(data=data)


def get_enrich_account_by_external_id(
        external_id: str, offset: int = 0, limit: int = 100
) -> PaginatedAccountsListResponse:
    return CloudInsightsServiceAPI().get_enrich_account_by_external_id(
        external_id=external_id, offset=offset, limit=limit
    )


def start_enrichment(cloud_insights_account_id: str, start_enrich: StartEnrich) -> str:
    return CloudInsightsServiceAPI().start_enrichment(
        cloud_insights_account_id=cloud_insights_account_id, start_enrich=start_enrich
    )


def start_async_enrichment(cloud_insights_account_id: str, start_enrich: StartEnrich) -> str:
    return CloudInsightsServiceAPI().start_async_enrichment(
        cloud_insights_account_id=cloud_insights_account_id, start_enrich=start_enrich
    )


def get_cloud_insight_account(account_id: str) -> CloudInsightAccount:
    return CloudInsightsServiceAPI().get_cloud_insight_account(account_id=account_id)


def delete_cloud_insight_account(account_id: str) -> bool:
    return CloudInsightsServiceAPI().delete_cloud_insight_account(account_id=account_id)


def get_account_logs(
        account_id: str, event_type: str, status: str, description: str, created_at_start: str, created_at_end: str
) -> PaginatedAccountLogsListResponse:
    return CloudInsightsServiceAPI().get_account_logs(
        account_id=account_id, event_type=event_type, status=status, description=description,
        created_at_start=created_at_start, created_at_end=created_at_end
    )


def get_all_containers_for_an_account_id(
        account_id: str, limit: int = 100, offset: int = 0, image_name: str = None, image_short_name: str = None,
        project_name: str = None, repo_url: str = None, cluster_name: str = None, public_exposed: str = None,
        search: str = None, cluster_id: str = None, order_column: str = None, order_direction: str = None
) -> PaginatedContainersListResponse:
    return CloudInsightsServiceAPI().get_all_containers_for_an_account_id(
        account_id=account_id, limit=limit, offset=offset, image_name=image_name, image_short_name=image_short_name,
        project_name=project_name, repo_url=repo_url, cluster_name=cluster_name, public_exposed=public_exposed,
        search=search, cluster_id=cluster_id, order_column=order_column, order_direction=order_direction,
    )


def get_resources_filtered_by_group(
        account_id: str, image_name: str = None, image_short_name: str = None, public_exposed: str = None,
        search: str = None, cluster_names: List[str] = None, asset_types: List[str] = None, resource_type: str = None,
        offset: int = 0, limit: int = 100, order_column: str = None, order_direction: str = None,
) -> PaginatedResourcesList:
    return CloudInsightsServiceAPI().get_resources_filtered_by_group(
        account_id=account_id, image_name=image_name, image_short_name=image_short_name, public_exposed=public_exposed,
        search=search, cluster_names=cluster_names, asset_types=asset_types, resource_type=resource_type,
        offset=offset, limit=limit, order_column=order_column, order_direction=order_direction,
    )
