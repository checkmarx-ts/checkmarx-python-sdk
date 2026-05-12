from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from typing import List
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import OK
from .dto import (
    CloudInsightCreateEnrichAccount,
    CloudInsightEnrichAccount,
    CloudInsightAccount,
    StartEnrich,
    PaginatedAccountLogsListResponse,
    PaginatedAccountsListResponse,
    PaginatedContainersListResponse,
    PaginatedResourcesList,
)


class CloudInsightsServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{self.api_client.configuration.server_base_url}/api/cnas"

    def create_enrich_account(
        self, data: CloudInsightCreateEnrichAccount
    ) -> CloudInsightEnrichAccount:
        """
        Args:
            data (CloudInsightCreateEnrichAccount):

        Returns:
            CloudInsightEnrichAccount
        """
        url = f"{self.base_url}/accounts/enrich"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(data)
        )
        return CloudInsightEnrichAccount.from_dict(response.json())

    def get_enrich_account_by_external_id(
        self, external_id: str, offset: int = 0, limit: int = 100
    ) -> PaginatedAccountsListResponse:
        """
        Args:
            external_id (str): A unique identifier provided by Checkmarx
            offset (int): Offset the results. Default value: 0
            limit (int): Limit the number of results

        Returns:
            PaginatedAccountsListResponse
        """
        url = f"{self.base_url}/accounts/enrich"
        params = {"external-id": external_id, "offset": offset, "limit": limit}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PaginatedAccountsListResponse.from_dict(response.json())

    def start_enrichment(
        self, cloud_insights_account_id: str, start_enrich: StartEnrich
    ) -> str:
        """
        Args:
            cloud_insights_account_id (str): uuid4
            start_enrich (StartEnrich):

        Returns:
            message (str)
        """
        url = f"{self.base_url}/accounts/{cloud_insights_account_id}/enrich"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(start_enrich)
        )
        return response.json().get("message")

    def start_async_enrichment(
        self, cloud_insights_account_id: str, start_enrich: StartEnrich
    ) -> str:
        """
        Args:
            cloud_insights_account_id (str): uuid4
            start_enrich (StartEnrich):

        Returns:
            syncId (str)
        """
        url = f"{self.base_url}/v2/accounts/{cloud_insights_account_id}/enrich"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(start_enrich)
        )
        return response.json().get("syncId")

    def get_cloud_insight_account(self, account_id: str) -> CloudInsightAccount:
        """
        Args:
            account_id (str): Cloud Insights account ID

        Returns:
            CloudInsightAccount
        """
        url = f"{self.base_url}/accounts/{account_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return CloudInsightAccount.from_dict(response.json())

    def delete_cloud_insight_account(self, account_id: str) -> bool:
        """
        Args:
            account_id (str): Cloud Insights account ID

        Returns:
            bool
        """
        url = f"{self.base_url}/accounts/{account_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == OK

    def get_account_logs(
        self,
        account_id: str,
        event_type: str,
        status: str,
        description: str,
        created_at_start: str,
        created_at_end: str,
    ) -> PaginatedAccountLogsListResponse:
        """
        Args:
            account_id (str): Cloud Insights account ID
            event_type (str): Available values: Incoming, Outgoing
            status (str): Available values: Success, Failed
            description (str): Available values: Sync, Scheduled
            created_at_start (str): Start of the creation date range in ISO
                8601 format (e.g., 2025-08-10T00:00:00Z).
            created_at_end (str): End of the creation date range in ISO 8601
                format (e.g., 2025-08-12T23:59:59Z).

        Returns:
            PaginatedAccountLogsListResponse
        """
        url = f"{self.base_url}/accounts/{account_id}/logs"
        params = {
            "eventType": event_type,
            "status": status,
            "description": description,
            "createdAtStart": created_at_start,
            "createdAtEnd": created_at_end,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PaginatedAccountLogsListResponse.from_dict(response.json())

    def get_all_containers_for_an_account_id(
        self,
        account_id: str,
        limit: int = 100,
        offset: int = 0,
        image_name: str = None,
        image_short_name: str = None,
        project_name: str = None,
        repo_url: str = None,
        cluster_name: str = None,
        public_exposed: str = None,
        search: str = None,
        cluster_id: str = None,
        order_column: str = None,
        order_direction: str = None,
    ) -> PaginatedContainersListResponse:
        """
        Args:
            account_id (str): Cloud Insights account ID
            limit (int): Limit the number of results
            offset (int): Offset the results. Default value: 0
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
        url = f"{self.base_url}/accounts/{account_id}/containers"
        params = {
            "limit": limit,
            "offset": offset,
            "image-name": image_name,
            "image-short-name": image_short_name,
            "project-name": project_name,
            "repo-url": repo_url,
            "cluster-name": cluster_name,
            "public-exposed": public_exposed,
            "search": search,
            "cluster-id": cluster_id,
            "order-column": order_column,
            "order-direction": order_direction,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PaginatedContainersListResponse.from_dict(response.json())

    def get_resources_filtered_by_group(
        self,
        account_id: str,
        image_name: str = None,
        image_short_name: str = None,
        public_exposed: str = None,
        search: str = None,
        cluster_names: List[str] = None,
        asset_types: List[str] = None,
        resource_type: str = None,
        offset: int = 0,
        limit: int = 100,
        order_column: str = None,
        order_direction: str = None,
    ) -> PaginatedResourcesList:
        """
        Args:
            account_id (str):
            image_name (str):
            image_short_name (str):
            public_exposed (str):
            search (str):
            cluster_names (List[str]): Filter by cluster names
                (comma-separated)
            asset_types (List[str]): Filter by asset types (comma-separated).
                Available values: ECS, Kubernetes
            resource_type (str): Available values: CONTAINER
            offset (int):
            limit (int):
            order_column (str):
            order_direction (str):

        Returns:
            PaginatedResourcesList
        """
        url = f"{self.base_url}/accounts/{account_id}/resources"
        params = {
            "image-name": image_name,
            "image-short-name": image_short_name,
            "public-exposed": public_exposed,
            "search": search,
            "cluster-name": ",".join(cluster_names) if cluster_names else None,
            "asset-type": ",".join(asset_types) if asset_types else None,
            "resource-type": resource_type,
            "offset": offset,
            "limit": limit,
            "order-column": order_column,
            "order-direction": order_direction,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PaginatedResourcesList.from_dict(response.json())


def create_enrich_account(
    data: CloudInsightCreateEnrichAccount,
) -> CloudInsightEnrichAccount:
    return CloudInsightsServiceAPI().create_enrich_account(data=data)


def get_enrich_account_by_external_id(
    external_id: str, offset: int = 0, limit: int = 100
) -> PaginatedAccountsListResponse:
    return CloudInsightsServiceAPI().get_enrich_account_by_external_id(
        external_id=external_id, offset=offset, limit=limit
    )


def start_enrichment(
    cloud_insights_account_id: str, start_enrich: StartEnrich
) -> str:
    return CloudInsightsServiceAPI().start_enrichment(
        cloud_insights_account_id=cloud_insights_account_id,
        start_enrich=start_enrich,
    )


def start_async_enrichment(
    cloud_insights_account_id: str, start_enrich: StartEnrich
) -> str:
    return CloudInsightsServiceAPI().start_async_enrichment(
        cloud_insights_account_id=cloud_insights_account_id,
        start_enrich=start_enrich,
    )


def get_cloud_insight_account(account_id: str) -> CloudInsightAccount:
    return CloudInsightsServiceAPI().get_cloud_insight_account(account_id=account_id)


def delete_cloud_insight_account(account_id: str) -> bool:
    return CloudInsightsServiceAPI().delete_cloud_insight_account(
        account_id=account_id
    )


def get_account_logs(
    account_id: str,
    event_type: str,
    status: str,
    description: str,
    created_at_start: str,
    created_at_end: str,
) -> PaginatedAccountLogsListResponse:
    return CloudInsightsServiceAPI().get_account_logs(
        account_id=account_id,
        event_type=event_type,
        status=status,
        description=description,
        created_at_start=created_at_start,
        created_at_end=created_at_end,
    )


def get_all_containers_for_an_account_id(
    account_id: str,
    limit: int = 100,
    offset: int = 0,
    image_name: str = None,
    image_short_name: str = None,
    project_name: str = None,
    repo_url: str = None,
    cluster_name: str = None,
    public_exposed: str = None,
    search: str = None,
    cluster_id: str = None,
    order_column: str = None,
    order_direction: str = None,
) -> PaginatedContainersListResponse:
    return CloudInsightsServiceAPI().get_all_containers_for_an_account_id(
        account_id=account_id,
        limit=limit,
        offset=offset,
        image_name=image_name,
        image_short_name=image_short_name,
        project_name=project_name,
        repo_url=repo_url,
        cluster_name=cluster_name,
        public_exposed=public_exposed,
        search=search,
        cluster_id=cluster_id,
        order_column=order_column,
        order_direction=order_direction,
    )


def get_resources_filtered_by_group(
    account_id: str,
    image_name: str = None,
    image_short_name: str = None,
    public_exposed: str = None,
    search: str = None,
    cluster_names: List[str] = None,
    asset_types: List[str] = None,
    resource_type: str = None,
    offset: int = 0,
    limit: int = 100,
    order_column: str = None,
    order_direction: str = None,
) -> PaginatedResourcesList:
    return CloudInsightsServiceAPI().get_resources_filtered_by_group(
        account_id=account_id,
        image_name=image_name,
        image_short_name=image_short_name,
        public_exposed=public_exposed,
        search=search,
        cluster_names=cluster_names,
        asset_types=asset_types,
        resource_type=resource_type,
        offset=offset,
        limit=limit,
        order_column=order_column,
        order_direction=order_direction,
    )
