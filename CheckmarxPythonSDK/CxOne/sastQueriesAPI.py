from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import QueriesResponse, Preset, QueryDescription, QueryDescriptionSampleCode, Category, CategoryType
from CheckmarxPythonSDK.utilities.compat import OK

query_url = "/api/queries"


class SastQueriesAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_list_of_the_existing_query_repos(self) -> List[QueriesResponse]:
        """

        Returns:
            List[QueriesResponse]
        """
        relative_url = query_url
        response = self.api_client.get_request(relative_url=relative_url)
        queries = response.json()
        return [
            QueriesResponse(
                name=item.get("name"),
                is_active=item.get("isActive"),
                last_modified=item.get("lastModified"),
            ) for item in queries
        ]

    def get_sast_queries_presets(self) -> List[Preset]:
        """

        Args:

        Returns:
            List[Preset]
        """
        relative_url = query_url + "/presets"
        response = self.api_client.get_request(relative_url=relative_url)
        presets = response.json()
        return [
            Preset(
                preset_id=item.get("id"),
                name=item.get("name"),
            ) for item in presets
        ]

    def get_sast_query_description(self, ids: List[str]) -> List[QueryDescription]:
        """

        Args:
            ids (List[str]): list of query ids

        Returns:
            List[QueryDescription]
             associated to each of the given query ids
        """
        type_check(ids, list)
        list_member_type_check(ids, str)

        relative_url = query_url + "/descriptions?"
        params = {"ids": ids}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return [
            QueryDescription(
                query_description_id=item.get("queryDescriptionId"),
                result_description=item.get("resultDescription"),
                risk=item.get("risk"),
                cause=item.get("cause"),
                general_recommendations=item.get("generalRecommendations"),
                samples=[
                    QueryDescriptionSampleCode(
                        programming_language=sample.get("progLanguage"),
                        code=sample.get("code"),
                        title=sample.get("title"),
                    ) for sample in item.get("samples") or []
                ],
            ) for item in response or []
        ]

    def get_mapping_between_ast_and_sast_query_ids(self) -> List[dict]:
        """

        Returns:
            List[dict]
            [
            {
              "astId": "string",
              "sastId": "string"
            }
          ]
        """
        result = None
        relative_url = query_url + "/mappings"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            result = response.json().get("mappings")
        return result

    def get_sast_queries_preset_for_a_specific_scan(self, scan_id: str) -> int:
        """

        Args:
            scan_id (str):

        Returns:
            prest_id (int)
        """
        result = None
        relative_url = query_url + f"/preset/{scan_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            result = response.json().get("id")
        return result

    def get_sast_queries_categories(self) -> List[CategoryType]:
        """

        Returns:
            List[CategoryType]
        """
        result = None
        relative_url = query_url + "/categories-types"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            response = response.json()
            result = [
                CategoryType(
                    category_type_id=item.get("id"),
                    name=item.get("name"),
                    sast_id=item.get("sastId"),
                    order=item.get("order"),
                    categories=[
                        Category(
                            category_id=category.get("id"),
                            name=category.get("name"),
                            sast_id=category.get("sastId"),
                        ) for category in item.get("categories", []) or []
                    ]
                ) for item in response
            ]
        return result


def get_list_of_the_existing_query_repos() -> List[QueriesResponse]:
    return SastQueriesAPI().get_list_of_the_existing_query_repos()


def get_sast_queries_presets() -> List[Preset]:
    return SastQueriesAPI().get_sast_queries_presets()


def get_sast_query_description(ids: List[str]) -> List[QueryDescription]:
    return SastQueriesAPI().get_sast_query_description(ids=ids)


def get_mapping_between_ast_and_sast_query_ids() -> List[dict]:
    return SastQueriesAPI().get_mapping_between_ast_and_sast_query_ids()


def get_sast_queries_preset_for_a_specific_scan(scan_id: str) -> int:
    return SastQueriesAPI().get_sast_queries_preset_for_a_specific_scan(scan_id=scan_id)


def get_sast_queries_categories() -> List[CategoryType]:
    return SastQueriesAPI().get_sast_queries_categories()
