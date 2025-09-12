import json
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from requests import Response
from ..utilities import type_check
from .url import api_url


class ClientRoleMappingsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def add_group_role(
            self, realm: str, group_id: str, container_id: str, role_id: str, role_name: str
    ) -> Response:
        type_check(realm, str)
        type_check(group_id, str)
        type_check(role_name, str)
        type_check(role_id, str)

        relative_url = api_url + f"/{realm}/groups/{group_id}/role-mappings/clients/{container_id}"
        post_data = json.dumps(
            [{
                "clientRole": True,
                "composite": True,
                "containerId": f"{container_id}",
                "description": "Scan projects in Groups of this user",
                "id": f"{role_id}",
                "name": f"{role_name}"
            }]
        )
        response = self.api_client.post_request(relative_url=relative_url, data=post_data)
        return response


def add_group_role(
        realm: str, group_id: str, container_id: str, role_id: str, role_name: str
) -> Response:
    return ClientRoleMappingsAPI().add_group_role(
        realm=realm, group_id=group_id, container_id=container_id, role_id=role_id, role_name=role_name
    )
