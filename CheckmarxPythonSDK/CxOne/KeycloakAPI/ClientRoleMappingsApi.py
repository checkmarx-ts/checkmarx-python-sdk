from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.RoleRepresentation import RoleRepresentation
from .api_url import api_url


class ClientRoleMappingsApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_group_role_mappings_client(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get client-level role mappings for the user, and the app
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/role_mappings/clients/{client}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_group_role_mappings_client(self, realm: str, id: str, client: str,
                                        role_representation: RoleRepresentation) -> bool:
        """
        Add client-level roles to the user role mapping
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/role_mappings/clients/{client}"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_group_role_mappings_client(self, realm: str, id: str, client: str) -> bool:
        """
        Delete client-level roles from user role mapping
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/role_mappings/clients/{client}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_group_role_mappings_client_available(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get available client-level roles that can be mapped to the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/clients/{client}/available
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/role_mappings/clients/{client}/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_group_role_mappings_client_composite(self, realm: str, id: str, client: str,
                                                 brief_representation: bool = None) -> List[RoleRepresentation]:
        """
        Get effective client-level role mappings This recurses any composite roles
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/clients/{client}/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/groups/{id}/role_mappings/clients/{client}/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_user_role_mappings_client(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get client-level role mappings for the user, and the app
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/role-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/role_mappings/clients/{client}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_user_role_mappings_client(self, realm: str, id: str, client: str,
                                       role_representation: RoleRepresentation) -> bool:
        """
        Add client-level roles to the user role mapping
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/role-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/role_mappings/clients/{client}"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_user_role_mappings_client(self, realm: str, id: str, client: str) -> bool:
        """
        Delete client-level roles from user role mapping
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/role-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/role_mappings/clients/{client}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_user_role_mappings_client_available(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get available client-level roles that can be mapped to the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/role-mappings/clients/{client}/available
        """
        relative_url = f"{api_url}/{realm}/users/{id}/role_mappings/clients/{client}/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_user_role_mappings_client_composite(self, realm: str, id: str, client: str,
                                                brief_representation: bool = None) -> List[RoleRepresentation]:
        """
        Get effective client-level role mappings This recurses any composite roles
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/role-mappings/clients/{client}/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/users/{id}/role_mappings/clients/{client}/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]
