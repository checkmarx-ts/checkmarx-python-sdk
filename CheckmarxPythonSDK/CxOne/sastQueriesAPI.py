from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    QueriesResponse,
    Preset,
    QueryDescription,
    CategoryType,
)
from CheckmarxPythonSDK.utilities.compat import OK


class SastQueriesAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/queries"
        )

    def get_list_of_the_existing_query_repos(
        self,
    ) -> List[QueriesResponse]:
        """
        Returns:
            List[QueriesResponse]
        """
        response = self.api_client.call_api(
            method="GET", url=self.base_url
        )
        return [
            QueriesResponse.from_dict(item)
            for item in (response.json() or [])
        ]

    def get_sast_queries_presets(self) -> List[Preset]:
        """
        Returns:
            List[Preset]
        """
        url = f"{self.base_url}/presets"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            Preset.from_dict(item) for item in (response.json() or [])
        ]

    def get_sast_query_description(
        self, ids: List[str]
    ) -> List[QueryDescription]:
        """
        Args:
            ids (List[str]): list of query ids.

        Returns:
            List[QueryDescription]
        """
        url = f"{self.base_url}/descriptions"
        params = {"ids": ids}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [
            QueryDescription.from_dict(item)
            for item in (response.json() or [])
        ]

    def get_mapping_between_ast_and_sast_query_ids(
        self,
    ) -> List[dict]:
        """
        Returns:
            List[dict]
        """
        url = f"{self.base_url}/mappings"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return response.json().get("mappings")
        return None

    def get_sast_queries_preset_for_a_specific_scan(
        self, scan_id: str
    ) -> int:
        """
        Args:
            scan_id (str):

        Returns:
            preset_id (int)
        """
        url = f"{self.base_url}/preset/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return response.json().get("id")
        return None

    def get_sast_queries_categories(self) -> List[CategoryType]:
        """
        Returns:
            List[CategoryType]
        """
        url = f"{self.base_url}/categories-types"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return [
                CategoryType.from_dict(item)
                for item in response.json()
            ]
        return None


def get_list_of_the_existing_query_repos() -> List[QueriesResponse]:
    return SastQueriesAPI().get_list_of_the_existing_query_repos()


def get_sast_queries_presets() -> List[Preset]:
    return SastQueriesAPI().get_sast_queries_presets()


def get_sast_query_description(
    ids: List[str],
) -> List[QueryDescription]:
    return SastQueriesAPI().get_sast_query_description(ids=ids)


def get_mapping_between_ast_and_sast_query_ids() -> List[dict]:
    return SastQueriesAPI().get_mapping_between_ast_and_sast_query_ids()


def get_sast_queries_preset_for_a_specific_scan(scan_id: str) -> int:
    return SastQueriesAPI().get_sast_queries_preset_for_a_specific_scan(
        scan_id=scan_id
    )


def get_sast_queries_categories() -> List[CategoryType]:
    return SastQueriesAPI().get_sast_queries_categories()
