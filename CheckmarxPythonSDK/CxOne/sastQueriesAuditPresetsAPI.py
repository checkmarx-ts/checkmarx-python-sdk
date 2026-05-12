from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    PresetPaged,
    PresetSummary,
    QueryDetails,
    Preset,
)
from CheckmarxPythonSDK.utilities.compat import OK


class SastQueriesAuditPresetsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/presets"
        )

    def get_presets(
        self,
        offset: int = 0,
        limit: int = 10,
        exact_match: bool = False,
        include_details: bool = False,
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
        params = {
            "offset": offset,
            "limit": limit,
            "exact_match": exact_match,
            "include_details": include_details,
            "name": name,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        if response.status_code == OK:
            return PresetPaged.from_dict(response.json())
        return None

    def create_new_preset(
        self, name: str, description: str, query_ids: List[str]
    ) -> dict:
        """
        Args:
            name (str):
            description (str):
            query_ids (list of str):

        Returns:
            dict
        """
        url = f"{self.base_url}/"
        data = {
            "name": name,
            "description": description,
            "queryIds": query_ids,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        if response.status_code == OK:
            resp = response.json()
            return {
                "id": int(resp.get("id")),
                "message": resp.get("message"),
            }
        return None

    def get_queries(self) -> List[QueryDetails]:
        """
        Returns:
            List[QueryDetails]
        """
        url = f"{self.base_url}/queries"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return [
                QueryDetails.from_dict(q)
                for q in (response.json() or [])
            ]
        return None

    def get_preset_by_id(self, preset_id: int) -> Preset:
        """
        Args:
            preset_id (int):

        Returns:
            Preset
        """
        url = f"{self.base_url}/{preset_id}"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return Preset.from_dict(response.json())
        return None

    def update_a_preset(
        self,
        preset_id: int,
        name: str,
        description: str = None,
        query_ids: List[str] = None,
    ) -> dict:
        """
        Args:
            preset_id (int):
            name (str):
            description (str):
            query_ids (list of str):

        Returns:
            dict
        """
        url = f"{self.base_url}/{preset_id}"
        data = {"name": name}
        if description:
            data["description"] = description
        if query_ids:
            data["queryIds"] = query_ids
        response = self.api_client.call_api(
            method="PUT", url=url, json=data
        )
        if response.status_code == OK:
            resp = response.json()
            return {
                "id": resp.get("id"),
                "message": resp.get("message"),
            }
        return None

    def delete_a_preset_by_id(self, preset_id: int) -> bool:
        """
        Args:
            preset_id (int):

        Returns:
            bool
        """
        url = f"{self.base_url}/{preset_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == OK

    def get_preset_summary_by_id(self, preset_id: int) -> PresetSummary:
        """
        Args:
            preset_id (int):

        Returns:
            PresetSummary
        """
        url = f"{self.base_url}/{preset_id}/summary"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return PresetSummary.from_dict(response.json())
        return None

    def clone_preset(
        self, preset_id: int, name: str, description: str
    ) -> dict:
        """
        Args:
            preset_id (int):
            name (str):
            description (str):

        Returns:
            dict
        """
        url = f"{self.base_url}/{preset_id}/clone"
        data = {"name": name, "description": description}
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        if response.status_code == OK:
            resp = response.json()
            return {
                "id": resp.get("id"),
                "message": resp.get("message"),
            }
        return None

    def add_query_to_preset(
        self, preset_id: int, query_path: str
    ) -> dict:
        """
        Args:
            preset_id (int):
            query_path (str):

        Returns:
            dict
        """
        url = f"{self.base_url}/{preset_id}/add-query"
        data = {"queryPath": query_path}
        response = self.api_client.call_api(
            method="PUT", url=url, json=data
        )
        if response.status_code == OK:
            resp = response.json()
            return {
                "id": resp.get("id"),
                "message": resp.get("message"),
            }
        return None


def get_presets(
    offset: int = 0,
    limit: int = 10,
    exact_match: bool = False,
    include_details: bool = False,
    name: str = None,
) -> PresetPaged:
    return SastQueriesAuditPresetsAPI().get_presets(
        offset=offset,
        limit=limit,
        exact_match=exact_match,
        include_details=include_details,
        name=name,
    )


def create_new_preset(
    name: str, description: str, query_ids: List[str]
) -> dict:
    return SastQueriesAuditPresetsAPI().create_new_preset(
        name=name, description=description, query_ids=query_ids
    )


def get_queries() -> List[QueryDetails]:
    return SastQueriesAuditPresetsAPI().get_queries()


def get_preset_by_id(preset_id: int) -> Preset:
    return SastQueriesAuditPresetsAPI().get_preset_by_id(
        preset_id=preset_id
    )


def update_a_preset(
    preset_id: int,
    name: str,
    description: str = None,
    query_ids: List[str] = None,
) -> dict:
    return SastQueriesAuditPresetsAPI().update_a_preset(
        preset_id=preset_id,
        name=name,
        description=description,
        query_ids=query_ids,
    )


def delete_a_preset_by_id(preset_id: int) -> bool:
    return SastQueriesAuditPresetsAPI().delete_a_preset_by_id(
        preset_id=preset_id
    )


def get_preset_summary_by_id(preset_id: int) -> PresetSummary:
    return SastQueriesAuditPresetsAPI().get_preset_summary_by_id(
        preset_id=preset_id
    )


def clone_preset(preset_id: int, name: str, description: str) -> dict:
    return SastQueriesAuditPresetsAPI().clone_preset(
        preset_id=preset_id, name=name, description=description
    )


def add_query_to_preset(preset_id: int, query_path: str) -> dict:
    return SastQueriesAuditPresetsAPI().add_query_to_preset(
        preset_id=preset_id, query_path=query_path
    )
