from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from ..utilities import type_check
from .url import api_url


class RoleMapperAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_role_mappings(self, realm: str, group_id: str) -> dict:
        type_check(realm, str)
        type_check(group_id, str)

        relative_url = api_url + f"/{realm}/groups/{group_id}/role-mappings"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        response = response.json()
        return response


def get_role_mappings(realm: str, group_id: str) -> dict:
    return RoleMapperAPI().get_role_mappings(realm=realm, group_id=group_id)
