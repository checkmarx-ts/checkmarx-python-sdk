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

    def get_keys(self, realm: str) -> KeysMetadataRepresentation:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            KeysMetadataRepresentation
        
        URL:
            Relative path: /{realm}/keys
        """
        relative_url = f"{api_url}/{realm}/keys"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return KeysMetadataRepresentation.from_dict(response.json())
