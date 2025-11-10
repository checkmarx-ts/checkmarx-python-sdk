from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.GroupRepresentation import GroupRepresentation
from .dto.ManagementPermissionReference import ManagementPermissionReference
from .dto.RoleRepresentation import RoleRepresentation
from .dto.UserRepresentation import UserRepresentation
from .api_url import api_url


class RolesApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_client_roles(self, realm: str, id: str, brief_representation: str = None, first: str = None,
                         max: str = None, search: str = None) -> List[RoleRepresentation]:
        """
        Get all roles for the realm or client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (str): 
            first (str): 
            max (str): 
            search (str): 
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/roles
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max, "search": search}
        relative_url = f"{api_url}/{realm}/clients/{id}/roles"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_roles(self, realm: str, id: str, role_representation: RoleRepresentation) -> bool:
        """
        Create a new role for the realm or client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/roles
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_client_role(self, realm: str, id: str, role_name: str) -> RoleRepresentation:
        """
        Get a role by name
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
        
        Returns:
            RoleRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return RoleRepresentation.from_dict(response.json())

    def put_client_role(self, realm: str, id: str, role_name: str, role_representation: RoleRepresentation) -> bool:
        """
        Update a role by name
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}"
        response = self.api_client.put_request(relative_url=relative_url, json=role_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_client_role(self, realm: str, id: str, role_name: str) -> bool:
        """
        Delete a role by name
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_role_composites(self, realm: str, id: str, role_name: str) -> List[RoleRepresentation]:
        """
        Get composites of the role
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/composites
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/composites"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_role_composites(self, realm: str, id: str, role_name: str,
                                    role_representation: RoleRepresentation) -> bool:
        """
        Add a composite to the role
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/composites
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/composites"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_role_composites(self, realm: str, id: str, role_name: str) -> bool:
        """
        Remove roles from the role’s composite
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/composites
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/composites"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_role_composites_client(self, realm: str, id: str, role_name: str, client_uuid: str) -> List[
        RoleRepresentation]:
        """
        Get client-level roles for the client that are in the role’s composite
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
            client_uuid (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/composites/clients/{clientUuid}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/composites/clients/{client_uuid}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_role_composites_realm(self, realm: str, id: str, role_name: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles of the role’s composite
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/composites/realm
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/composites/realm"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_role_groups(self, realm: str, id: str, role_name: str, brief_representation: bool = None,
                               first: bool = None, max: bool = None) -> List[GroupRepresentation]:
        """
        Returns a stream of groups that have the specified role name
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
            brief_representation (bool): if false, return a full representation of the {@code GroupRepresentation} objects.
            first (bool): first result to return. Ignored if negative or {@code null}.
            max (bool): maximum number of results to return. Ignored if negative or {@code null}.
        
        Returns:
            List[GroupRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/groups
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max}
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/groups"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [GroupRepresentation.from_dict(item) for item in response.json()]

    def get_client_role_management_permissions(self, realm: str, id: str,
                                               role_name: str) -> ManagementPermissionReference:
        """
        Return object stating whether role Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_client_role_management_permissions(self, realm: str, id: str, role_name: str,
                                               management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        Return object stating whether role Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/management/permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def get_client_role_users(self, realm: str, id: str, role_name: str, first: bool = None, max: bool = None) -> List[
        UserRepresentation]:
        """
        Returns a stream of users that have the specified role name.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_name (str):  [required]
            first (bool): first result to return. Ignored if negative or {@code null}.
            max (bool): maximum number of results to return. Ignored if negative or {@code null}.
        
        Returns:
            List[UserRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/roles/{role_name}/users
        """
        params = {"first": first, "max": max}
        relative_url = f"{api_url}/{realm}/clients/{id}/roles/{role_name}/users"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [UserRepresentation.from_dict(item) for item in response.json()]

    def get_roles_by_realm(self, realm: str, brief_representation: str = None, first: str = None, max: str = None,
                           search: str = None) -> List[RoleRepresentation]:
        """
        Get all roles for the realm or client
        
        Args:
            realm (str):  [required]
            brief_representation (str): 
            first (str): 
            max (str): 
            search (str): 
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max, "search": search}
        relative_url = f"{api_url}/{realm}/roles"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_roles_by_realm(self, realm: str, role_representation: RoleRepresentation) -> bool:
        """
        Create a new role for the realm or client
        
        Args:
            realm (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles
        """
        relative_url = f"{api_url}/{realm}/roles"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_role_by_realm_by_role_name(self, realm: str, role_name: str) -> RoleRepresentation:
        """
        Get a role by name
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
        
        Returns:
            RoleRepresentation
        
        URL:
            Relative path: /{realm}/roles/{role_name}
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return RoleRepresentation.from_dict(response.json())

    def put_role_by_realm_by_role_name(self, realm: str, role_name: str,
                                       role_representation: RoleRepresentation) -> bool:
        """
        Update a role by name
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles/{role_name}
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}"
        response = self.api_client.put_request(relative_url=relative_url, json=role_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_role_by_realm_by_role_name(self, realm: str, role_name: str) -> bool:
        """
        Delete a role by name
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles/{role_name}
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_role_composites_by_realm_by_role_name(self, realm: str, role_name: str) -> List[RoleRepresentation]:
        """
        Get composites of the role
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles/{role_name}/composites
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/composites"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_role_composites_by_realm_by_role_name(self, realm: str, role_name: str,
                                                   role_representation: RoleRepresentation) -> bool:
        """
        Add a composite to the role
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles/{role_name}/composites
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/composites"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_role_composites_by_realm_by_role_name(self, realm: str, role_name: str) -> bool:
        """
        Remove roles from the role’s composite
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/roles/{role_name}/composites
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/composites"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_role_composites_client_by_realm_by_role_name_by_client_uuid(self, realm: str, role_name: str,
                                                                        client_uuid: str) -> List[RoleRepresentation]:
        """
        Get client-level roles for the client that are in the role’s composite
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
            client_uuid (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles/{role_name}/composites/clients/{clientUuid}
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/composites/clients/{client_uuid}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_role_composites_realm_by_realm_by_role_name(self, realm: str, role_name: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles of the role’s composite
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/roles/{role_name}/composites/realm
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/composites/realm"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_role_groups_by_realm_by_role_name(self, realm: str, role_name: str, brief_representation: bool = None,
                                              first: bool = None, max: bool = None) -> List[GroupRepresentation]:
        """
        Returns a stream of groups that have the specified role name
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
            brief_representation (bool): if false, return a full representation of the {@code GroupRepresentation} objects.
            first (bool): first result to return. Ignored if negative or {@code null}.
            max (bool): maximum number of results to return. Ignored if negative or {@code null}.
        
        Returns:
            List[GroupRepresentation]
        
        URL:
            Relative path: /{realm}/roles/{role_name}/groups
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max}
        relative_url = f"{api_url}/{realm}/roles/{role_name}/groups"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [GroupRepresentation.from_dict(item) for item in response.json()]

    def get_role_management_permissions_by_realm_by_role_name(self, realm: str,
                                                              role_name: str) -> ManagementPermissionReference:
        """
        Return object stating whether role Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/roles/{role_name}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_role_management_permissions_by_realm_by_role_name(self, realm: str, role_name: str,
                                                              management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        Return object stating whether role Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/roles/{role_name}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/roles/{role_name}/management/permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def get_role_users_by_realm_by_role_name(self, realm: str, role_name: str, first: bool = None, max: bool = None) -> \
    List[UserRepresentation]:
        """
        Returns a stream of users that have the specified role name.
        
        Args:
            realm (str):  [required]
            role_name (str):  [required]
            first (bool): first result to return. Ignored if negative or {@code null}.
            max (bool): maximum number of results to return. Ignored if negative or {@code null}.
        
        Returns:
            List[UserRepresentation]
        
        URL:
            Relative path: /{realm}/roles/{role_name}/users
        """
        params = {"first": first, "max": max}
        relative_url = f"{api_url}/{realm}/roles/{role_name}/users"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [UserRepresentation.from_dict(item) for item in response.json()]
