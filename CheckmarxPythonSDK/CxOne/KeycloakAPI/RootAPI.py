from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .url import api_url
from .dto import RealmRepresentation, construct_realm_representation
from typing import List


class RootAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_realms(self) -> List[RealmRepresentation]:
        """

        Returns:
            list of RealmRepresentation
        """
        relative_url = api_url
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        realms = response.json()
        return [construct_realm_representation(realm) for realm in realms]


def get_realms() -> List[RealmRepresentation]:
    return RootAPI().get_realms()
