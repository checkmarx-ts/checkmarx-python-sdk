from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.ManagementPermissionReference import ManagementPermissionReference
from .dto.RoleRepresentation import RoleRepresentation
from .api_url import api_url


class RolesByIdApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_roles_by_id(self, realm: str, role_id: str) -> RoleRepresentation:
        """
        Get a specific role’s representation
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
        
        Returns:
            RoleRepresentation
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return RoleRepresentation.from_dict(response.json())

    def put_roles_by_id(self, realm: str, role_id: str, role_representation: RoleRepresentation) -> bool:
        """
        Update the role
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}"
        response = self.api_client.put_request(relative_url=relative_url, json=role_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 204

    def delete_roles_by_id(self, realm: str, role_id: str) -> bool:
        """
        Delete the role
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_roles_by_id_composites(self, realm: str, role_id: str, first: str = None, max: str = None,
                                   search: str = None) -> List[RoleRepresentation]:
        """
        Get role’s children Returns a set of role’s children provided the role is a composite.
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
            first (str): 
            max (str): 
            search (str): 
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/composites
        """
        params = {"first": first, "max": max, "search": search}
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/composites"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_roles_by_id_composites(self, realm: str, role_id: str, role_representation: RoleRepresentation) -> bool:
        """
        Make the role a composite role by associating some child roles
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/composites
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/composites"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_roles_by_id_composites(self, realm: str, role_id: str) -> bool:
        """
        Remove a set of roles from the role’s composite
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/composites
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/composites"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_roles_by_id_composites_client(self, realm: str, role_id: str, client_uuid: str) -> List[RoleRepresentation]:
        """
        Get client-level roles for the client that are in the role’s composite
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
            client_uuid (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/composites/clients/{clientUuid}
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/composites/clients/{client_uuid}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_roles_by_id_composites_realm(self, realm: str, role_id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles that are in the role’s composite
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/composites/realm
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/composites/realm"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_roles_by_id_management_permissions(self, realm: str, role_id: str) -> ManagementPermissionReference:
        """
        Return object stating whether role Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_roles_by_id_management_permissions(self, realm: str, role_id: str,
                                               management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        Return object stating whether role Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            role_id (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/roles-by-id/{role_id}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/roles_by_id/{role_id}/management/permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())
