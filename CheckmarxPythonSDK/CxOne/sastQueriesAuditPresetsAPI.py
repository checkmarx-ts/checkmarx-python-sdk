from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import (
    PresetPaged, construct_preset_paged,
    PresetSummary, construct_preset_summary,
    QueryDetails, construct_query_details,
    Preset, construct_preset
)
from CheckmarxPythonSDK.utilities.compat import OK

api_url = "/api/presets"


class SastQueriesAuditPresetsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_presets(
            self, offset: int = 0, limit: int = 10, exact_match: bool = False, include_details: bool = False,
            name: str = None,
    ) -> PresetPaged:
        """

        Args:
            offset (int):
            limit (int):
            exact_match (bool):
            include_details (bool):
            name (str):

        Returns:
            PresetPaged
        """
        result = None
        type_check(offset, int)
        type_check(limit, int)
        type_check(exact_match, bool)
        type_check(include_details, bool)
        type_check(name, str)

        relative_url = api_url
        params = {
            "offset": offset, "limit": limit, "exact_match": exact_match, "include_details": include_details,
            "name": name
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        if response.status_code == OK:
            response = response.json()
            result = construct_preset_paged(response)
        return result

    def create_new_preset(self, name: str, description: str, query_ids: List[str]) -> dict:
        """

        Args:
            name (str):
            description (str):
            query_ids (list of str):

        Returns:
            dict
        """
        result = None
        type_check(name, str)
        type_check(description, str)
        type_check(query_ids, list)
        list_member_type_check(query_ids, str)

        relative_url = api_url + "/"
        data = {
            "name": name,
            "description": description,
            "queryIds": query_ids
        }

        response = self.api_client.post_request(relative_url=relative_url, json=data)
        if response.status_code == OK:
            response = response.json()
            result = {
                "id": int(response.get("id")),
                "message": response.get("message")
            }
        return result

    def get_queries(self) -> List[QueryDetails]:
        """

        Returns:
            List[QueryDetails]
        """
        result = None
        relative_url = api_url + "/queries"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            response = response.json()
            result = [
                construct_query_details(query) for query in response or []
            ]
        return result

    def get_preset_by_id(self, preset_id: int) -> Preset:
        """

        Args:
            preset_id (int):

        Returns:
            Preset
        """
        result = None
        type_check(preset_id, int)
        relative_url = api_url + f"/{preset_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            response = response.json()
            result = construct_preset(response)
        return result

    def update_a_preset(self, preset_id: int, name: str, description: str = None, query_ids: List[str] = None) -> dict:
        """

        Args:
            preset_id (int):
            name (str):
            description (str):
            query_ids (list of str):

        Returns:
            dict
            {
              "id": 123456,
              "message": "preset saved"
            }
        """
        result = None
        type_check(preset_id, int)
        type_check(name, str)
        type_check(description, str)
        type_check(query_ids, list)
        list_member_type_check(query_ids, str)

        relative_url = api_url + f"/{preset_id}"

        data = {"name": name, }
        if description:
            data.update({"description": description, })
        if query_ids:
            data.update({"queryIds": query_ids, })
        response = self.api_client.put_request(relative_url=relative_url, json=data)
        if response.status_code == OK:
            response = response.json()
            result = {
                "id": response.get("id"),
                "message": response.get("message"),
            }
        return result

    def delete_a_preset_by_id(self, preset_id: int) -> bool:
        """

       Args:
           preset_id (int):

       Returns:
            bool
       """
        type_check(preset_id, int)
        relative_url = api_url + f"/{preset_id}"
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == OK

    def get_preset_summary_by_id(self, preset_id: int) -> PresetSummary:
        """

        Args:
            preset_id (int):

        Returns:
            PresetSummary
        """
        result = None
        type_check(preset_id, int)
        relative_url = api_url + f"/{preset_id}/summary"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            response = response.json()
            result = construct_preset_summary(response)
        return result

    def clone_preset(self, preset_id: int, name: str, description: str) -> dict:
        """

        Args:
            preset_id (int):
            name (str):
            description (str):

        Returns:
            dict
        """
        result = None
        type_check(preset_id, int)
        type_check(name, str)
        type_check(description, str)
        relative_url = api_url + f"/{preset_id}/clone"

        data = {
            "name": name,
            "description": description,
        }

        response = self.api_client.post_request(relative_url=relative_url, json=data)
        if response.status_code == OK:
            response = response.json()
            result = {
                "id": response.get("id"),
                "message": response.get("message"),
            }
        return result

    def add_query_to_preset(self, preset_id: int, query_path: str) -> dict:
        """

        Args:
            preset_id (int):
            query_path (str):

        Returns:
            dict
        """
        result = None
        type_check(preset_id, int)
        type_check(query_path, str)

        relative_url = api_url + f"/{preset_id}/add-query"
        data = {
            "queryPath": query_path,
        }
        response = self.api_client.put_request(relative_url=relative_url, json=data)
        if response.status_code == OK:
            response = response.json()
            result = {
                "id": response.get("id"),
                "message": response.get("message"),
            }
        return result


def get_presets(
        offset: int = 0, limit: int = 10, exact_match: bool = False, include_details: bool = False,
        name: str = None,
) -> PresetPaged:
    return SastQueriesAuditPresetsAPI().get_presets(
        offset=offset, limit=limit, exact_match=exact_match, include_details=include_details, name=name
    )


def create_new_preset(name: str, description: str, query_ids: List[str]) -> dict:
    return SastQueriesAuditPresetsAPI().create_new_preset(name=name, description=description, query_ids=query_ids)


def get_queries() -> List[QueryDetails]:
    return SastQueriesAuditPresetsAPI().get_queries()


def get_preset_by_id(preset_id: int) -> Preset:
    return SastQueriesAuditPresetsAPI().get_preset_by_id(preset_id=preset_id)


def update_a_preset(preset_id: int, name: str, description: str = None, query_ids: List[str] = None) -> dict:
    return SastQueriesAuditPresetsAPI().update_a_preset(
        preset_id=preset_id, name=name, description=description, query_ids=query_ids
    )


def delete_a_preset_by_id(preset_id: int) -> bool:
    return SastQueriesAuditPresetsAPI().delete_a_preset_by_id(preset_id=preset_id)


def get_preset_summary_by_id(preset_id: int) -> PresetSummary:
    return SastQueriesAuditPresetsAPI().get_preset_summary_by_id(preset_id=preset_id)


def clone_preset(preset_id: int, name: str, description: str) -> dict:
    return SastQueriesAuditPresetsAPI().clone_preset(preset_id=preset_id, name=name, description=description)


def add_query_to_preset(preset_id: int, query_path: str) -> dict:
    return SastQueriesAuditPresetsAPI().add_query_to_preset(preset_id=preset_id, query_path=query_path)
