from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.KeysMetadataRepresentation import KeysMetadataRepresentation
from .api_url import api_url


class KeyApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{api_client.configuration.iam_base_url.rstrip('/')}{api_url}"

    def get_keys(self, realm: str) -> KeysMetadataRepresentation:
        """

        Args:
            realm (str):  [required]

        Returns:
            KeysMetadataRepresentation

        URL:
            Relative path: /{realm}/keys
        """
        url = f"{self.base_url}/{realm}/keys"
        response = self.api_client.call_api("GET", url)
        return KeysMetadataRepresentation.from_dict(response.json())
