from requests import Response
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    CustomState, construct_custom_state
)

api_url = "/api/custom-states"


class CustomStateAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_custom_states(self, include_deleted: bool = False) -> List[CustomState]:
        """

        Args:
            include_deleted (bool):

        Returns:
            [
              {
                "id": 391,
                "name": "demo1",
                "type": "INFO",
                "isAllowed": true
              },
              {
                "id": 390,
                "name": "demo2",
                "type": "INFO",
                "isAllowed": false
              }
            ]
        """
        relative_url = api_url
        params = {"include-deleted": include_deleted}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return [
            construct_custom_state(custom_state) for custom_state in item or []
        ]

    def create_a_custom_state(self, name: str) -> Response:
        response = self.api_client.post_request(relative_url=api_url, json={"name": name})
        return response

    def delete_a_custom_state(self, custom_state_id: int) -> Response:
        relative_url = api_url + f"/{custom_state_id}"
        response = self.api_client.delete_request(relative_url=relative_url)
        return response


def get_all_custom_states(include_deleted: bool = False) -> List[CustomState]:
    return CustomStateAPI().get_all_custom_states(include_deleted=include_deleted)


def create_a_custom_state(name: str):
    return CustomStateAPI().create_a_custom_state(name=name)


def delete_a_custom_state(custom_state_id: int):
    return CustomStateAPI().delete_a_custom_state(custom_state_id=custom_state_id)
