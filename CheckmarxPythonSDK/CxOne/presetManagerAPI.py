from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class PresetManagerAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/preset-manager"
        )

    def get_sast_presets(
        self,
        scanner: str,
        limit: int = 10,
        offset: int = 0,
        fields: List[str] = None,
        sort: str = None,
        include_details: bool = False,
        search_term: str = None,
        exact_match: bool = False,
    ) -> dict:
        """
        List presets for a scanner.

        Args:
            scanner (str): 'sast' or 'iac'
            limit (int): Max results (1-100). Default: 10
            offset (int): Items to skip. Default: 0
            fields (List[str]): Fields to include
            sort (str): Sort expression (e.g. '-description')
            include_details (bool): Include detailed info. Default: False
            search_term (str): Filter by search term
            exact_match (bool): Require exact match. Default: False

        Returns:
            dict with totalFilteredCount, totalCount, presets
        """
        url = f"{self.base_url}/{scanner}/presets"
        params = {
            "limit": limit,
            "offset": offset,
            "fields": fields,
            "sort": sort,
            "include-details": include_details,
            "search-term": search_term,
            "exact-match": exact_match,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_sast_preset_by_id(self, scanner: str, id) -> dict:
        """
        Get a preset by ID.

        Args:
            scanner (str): 'sast' or 'iac'
            id (int or str): Preset identifier

        Returns:
            dict with id, name, description, custom, queries
        """
        url = f"{self.base_url}/{scanner}/presets/{id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def create_preset(self, scanner: str, name: str, queries: List[dict],
                      description: str = None) -> dict:
        """
        Create a new preset.

        Args:
            scanner (str): 'sast' or 'iac'
            name (str): Preset name (max 30 chars)
            queries (List[dict]): List of QueriesByFamily dicts
                with familyName, totalCount, queryIds
            description (str): Optional description

        Returns:
            dict with id and message
        """
        url = f"{self.base_url}/{scanner}/presets"
        body = {"name": name, "queries": queries}
        if description:
            body["description"] = description
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def update_preset(self, scanner: str, id, name: str,
                      queries: List[dict], description: str = None) -> dict:
        """
        Update a preset.

        Args:
            scanner (str): 'sast' or 'iac'
            id (int or str): Preset identifier
            name (str): Preset name (max 30 chars)
            queries (List[dict]): List of QueriesByFamily dicts
            description (str): Optional description

        Returns:
            dict with id and message
        """
        url = f"{self.base_url}/{scanner}/presets/{id}"
        body = {"name": name, "queries": queries}
        if description:
            body["description"] = description
        response = self.api_client.call_api(
            method="PUT", url=url, json=body
        )
        return response.json()

    def delete_preset(self, scanner: str, id) -> bool:
        """
        Delete a preset by ID.

        Args:
            scanner (str): 'sast' or 'iac'
            id (int or str): Preset identifier

        Returns:
            bool
        """
        url = f"{self.base_url}/{scanner}/presets/{id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == 200

    def clone_preset(self, scanner: str, id, name: str,
                     description: str = None) -> dict:
        """
        Clone a preset.

        Args:
            scanner (str): 'sast' or 'iac'
            id (int or str): Preset identifier to clone
            name (str): Name for the cloned preset (max 30 chars)
            description (str): Optional description (max 60 chars)

        Returns:
            dict with id and message
        """
        url = f"{self.base_url}/{scanner}/presets/{id}/clone"
        body = {"name": name}
        if description:
            body["description"] = description
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def get_query_families(self, scanner: str,
                           search_term: str = None) -> List[str]:
        """
        List the available query families for a scanner.

        Args:
            scanner (str): 'sast' or 'iac'
            search_term (str): Filter by search term

        Returns:
            list of str
        """
        url = f"{self.base_url}/{scanner}/query-families"
        params = {"search-term": search_term}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_queries_by_family(self, scanner: str, query_family: str,
                              search_term: str = None) -> List[dict]:
        """
        List the queries of a given family.

        Args:
            scanner (str): 'sast' or 'iac'
            query_family (str): Query family name (e.g. 'Apex')
            search_term (str): Filter by search term

        Returns:
            list of QueriesTree dicts
        """
        url = f"{self.base_url}/{scanner}/query-families/{query_family}/queries"
        params = {"search-term": search_term}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


# ---- Module-level convenience functions ----

def get_sast_presets(
    scanner: str,
    limit: int = 10,
    offset: int = 0,
    fields: List[str] = None,
    sort: str = None,
    include_details: bool = False,
    search_term: str = None,
    exact_match: bool = False,
) -> dict:
    return PresetManagerAPI().get_sast_presets(
        scanner=scanner, limit=limit, offset=offset, fields=fields,
        sort=sort, include_details=include_details,
        search_term=search_term, exact_match=exact_match,
    )


def get_sast_preset_by_id(scanner: str, id) -> dict:
    return PresetManagerAPI().get_sast_preset_by_id(scanner=scanner, id=id)


def create_sast_preset(scanner: str, name: str, queries: List[dict],
                          description: str = None) -> dict:
    return PresetManagerAPI().create_preset(
        scanner=scanner, name=name, queries=queries, description=description,
    )


def update_sast_preset(scanner: str, id, name: str, queries: List[dict],
                          description: str = None) -> dict:
    return PresetManagerAPI().update_preset(
        scanner=scanner, id=id, name=name, queries=queries,
        description=description,
    )


def delete_sast_preset(scanner: str, id) -> bool:
    return PresetManagerAPI().delete_preset(scanner=scanner, id=id)


def clone_sast_preset(scanner: str, id, name: str,
                         description: str = None) -> dict:
    return PresetManagerAPI().clone_preset(
        scanner=scanner, id=id, name=name, description=description,
    )


def get_sast_query_families(scanner: str, search_term: str = None) -> List[str]:
    return PresetManagerAPI().get_query_families(
        scanner=scanner, search_term=search_term,
    )


def get_sast_queries_by_family(
    scanner: str, query_family: str, search_term: str = None
) -> List[dict]:
    return PresetManagerAPI().get_queries_by_family(
        scanner=scanner, query_family=query_family, search_term=search_term,
    )
