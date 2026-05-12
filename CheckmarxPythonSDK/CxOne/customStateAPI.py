from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import CustomState


class CustomStateAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/custom-states"
        )

    def get_all_custom_states(
        self, include_deleted: bool = False
    ) -> List[CustomState]:
        """
        Args:
            include_deleted (bool):

        Returns:
            List[CustomState]
        """
        params = {"include-deleted": include_deleted}
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return [CustomState.from_dict(s) for s in (response.json() or [])]

    def create_a_custom_state(self, name: str):
        """
        Args:
            name (str):

        Returns:
            Response
        """
        response = self.api_client.call_api(
            method="POST", url=self.base_url, json={"name": name}
        )
        return response

    def delete_a_custom_state(self, custom_state_id: int):
        """
        Args:
            custom_state_id (int):

        Returns:
            Response
        """
        url = f"{self.base_url}/{custom_state_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response


def get_all_custom_states(include_deleted: bool = False) -> List[CustomState]:
    return CustomStateAPI().get_all_custom_states(include_deleted=include_deleted)


def create_a_custom_state(name: str):
    return CustomStateAPI().create_a_custom_state(name=name)


def delete_a_custom_state(custom_state_id: int):
    return CustomStateAPI().delete_a_custom_state(custom_state_id=custom_state_id)
