from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.ClientInitialAccessCreatePresentation import ClientInitialAccessCreatePresentation
from .dto.ClientInitialAccessPresentation import ClientInitialAccessPresentation
from .api_url import api_url


class ClientInitialAccessApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_clients_initial_access(self, realm: str) -> List[ClientInitialAccessPresentation]:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[ClientInitialAccessPresentation]
        
        URL:
            Relative path: /{realm}/clients-initial-access
        """
        relative_url = f"{api_url}/{realm}/clients_initial_access"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientInitialAccessPresentation.from_dict(item) for item in response.json()]

    def post_clients_initial_access(self, realm: str,
                                    client_initial_access_create_presentation: ClientInitialAccessCreatePresentation) -> ClientInitialAccessPresentation:
        """
        Create a new initial access token.
        
        Args:
            realm (str):  [required]
            client_initial_access_create_presentation (ClientInitialAccessCreatePresentation): Request body data [required]
        
        Returns:
            ClientInitialAccessPresentation
        
        URL:
            Relative path: /{realm}/clients-initial-access
        """
        relative_url = f"{api_url}/{realm}/clients_initial_access"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=client_initial_access_create_presentation.to_dict(), is_iam=True)
        return ClientInitialAccessPresentation.from_dict(response.json())

    def delete_clients_initial_acces(self, realm: str, id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients-initial-access/{id}
        """
        relative_url = f"{api_url}/{realm}/clients_initial_access/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204
