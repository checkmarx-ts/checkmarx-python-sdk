from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.ComponentTypeRepresentation import ComponentTypeRepresentation
from .api_url import api_url


class ClientRegistrationPolicyApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_providers(self, realm: str) -> List[ComponentTypeRepresentation]:
        """
        Base path for retrieve providers with the configProperties properly filled
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[ComponentTypeRepresentation]
        
        URL:
            Relative path: /{realm}/client-registration-policy/providers
        """
        relative_url = f"{api_url}/{realm}/client_registration_policy/providers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ComponentTypeRepresentation.from_dict(item) for item in response.json()]
