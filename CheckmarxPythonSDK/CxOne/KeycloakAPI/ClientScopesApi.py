from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.ClientScopeRepresentation import ClientScopeRepresentation
from .api_url import api_url


class ClientScopesApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_client_scopes(self, realm: str) -> List[ClientScopeRepresentation]:
        """
        Get client scopes belonging to the realm Returns a list of client scopes belonging to the realm
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[ClientScopeRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes
        """
        relative_url = f"{api_url}/{realm}/client_scopes"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientScopeRepresentation.from_dict(item) for item in response.json()]

    def post_client_scopes(self, realm: str, client_scope_representation: ClientScopeRepresentation) -> bool:
        """
        Create a new client scope Client Scope’s name must be unique!
        
        Args:
            realm (str):  [required]
            client_scope_representation (ClientScopeRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes
        """
        relative_url = f"{api_url}/{realm}/client_scopes"
        response = self.api_client.post_request(relative_url=relative_url, json=client_scope_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_client_scope(self, realm: str, id: str) -> ClientScopeRepresentation:
        """
        Get representation of the client scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            ClientScopeRepresentation
        
        URL:
            Relative path: /{realm}/client-scopes/{id}
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ClientScopeRepresentation.from_dict(response.json())

    def put_client_scope(self, realm: str, id: str, client_scope_representation: ClientScopeRepresentation) -> bool:
        """
        Update the client scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_scope_representation (ClientScopeRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes/{id}
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}"
        response = self.api_client.put_request(relative_url=relative_url, json=client_scope_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_client_scope(self, realm: str, id: str) -> bool:
        """
        Delete the client scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes/{id}
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_client_templates(self, realm: str) -> List[ClientScopeRepresentation]:
        """
        Get client scopes belonging to the realm Returns a list of client scopes belonging to the realm
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[ClientScopeRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates
        """
        relative_url = f"{api_url}/{realm}/client_templates"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientScopeRepresentation.from_dict(item) for item in response.json()]

    def post_client_templates(self, realm: str, client_scope_representation: ClientScopeRepresentation) -> bool:
        """
        Create a new client scope Client Scope’s name must be unique!
        
        Args:
            realm (str):  [required]
            client_scope_representation (ClientScopeRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates
        """
        relative_url = f"{api_url}/{realm}/client_templates"
        response = self.api_client.post_request(relative_url=relative_url, json=client_scope_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_client_template(self, realm: str, id: str) -> ClientScopeRepresentation:
        """
        Get representation of the client scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            ClientScopeRepresentation
        
        URL:
            Relative path: /{realm}/client-templates/{id}
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ClientScopeRepresentation.from_dict(response.json())

    def put_client_template(self, realm: str, id: str, client_scope_representation: ClientScopeRepresentation) -> bool:
        """
        Update the client scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_scope_representation (ClientScopeRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates/{id}
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}"
        response = self.api_client.put_request(relative_url=relative_url, json=client_scope_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_client_template(self, realm: str, id: str) -> bool:
        """
        Delete the client scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates/{id}
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200
