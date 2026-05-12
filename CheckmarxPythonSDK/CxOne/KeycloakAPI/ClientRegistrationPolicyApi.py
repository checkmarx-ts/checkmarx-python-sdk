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
        self.base_url = f"{api_client.configuration.iam_base_url.rstrip('/')}{api_url}"

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
        url = f"{self.base_url}/{realm}/client-registration-policy/providers"
        response = self.api_client.call_api("GET", url)
        return [ComponentTypeRepresentation.from_dict(item) for item in response.json()]
