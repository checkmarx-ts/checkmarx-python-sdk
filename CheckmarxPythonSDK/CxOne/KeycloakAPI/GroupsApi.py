from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.GroupRepresentation import GroupRepresentation
from .dto.ManagementPermissionReference import ManagementPermissionReference
from .dto.UserRepresentation import UserRepresentation
from .api_url import api_url


class GroupsApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_groups_by_realm(self, realm: str, brief_representation: str = None, exact: str = None, first: str = None,
                            max: str = None, populate_hierarchy: str = None, q: str = None, search: str = None) -> List[
        GroupRepresentation]:
        """
        Get group hierarchy.  Only name and ids are returned.
        
        Args:
            realm (str):  [required]
            brief_representation (str): 
            exact (str): 
            first (str): 
            max (str): 
            populate_hierarchy (str): 
            q (str): 
            search (str): 
        
        Returns:
            List[GroupRepresentation]
        
        URL:
            Relative path: /{realm}/groups
        """
        params = {"briefRepresentation": brief_representation, "exact": exact, "first": first, "max": max,
                  "populateHierarchy": populate_hierarchy, "q": q, "search": search}
        relative_url = f"{api_url}/{realm}/groups"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [GroupRepresentation.from_dict(item) for item in response.json()]

    def post_groups(self, realm: str, group_representation: GroupRepresentation) -> bool:
        """
        create or add a top level realm groupSet or create child.
        
        Args:
            realm (str):  [required]
            group_representation (GroupRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/groups
        """
        relative_url = f"{api_url}/{realm}/groups"
        response = self.api_client.post_request(relative_url=relative_url, json=group_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_groups_count_by_realm(self, realm: str, search: str = None, top: str = None) -> Dict[str, Any]:
        """
        Returns the groups counts.
        
        Args:
            realm (str):  [required]
            search (str): 
            top (str): 
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/groups/count
        """
        params = {"search": search, "top": top}
        relative_url = f"{api_url}/{realm}/groups/count"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return response.json()

    def get_group(self, realm: str, id: str) -> GroupRepresentation:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            GroupRepresentation
        
        URL:
            Relative path: /{realm}/groups/{id}
        """
        relative_url = f"{api_url}/{realm}/groups/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return GroupRepresentation.from_dict(response.json())

    def put_group_by_realm_by_id(self, realm: str, id: str, group_representation: GroupRepresentation) -> bool:
        """
        Update group, ignores subgroups.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            group_representation (GroupRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/groups/{id}
        """
        relative_url = f"{api_url}/{realm}/groups/{id}"
        response = self.api_client.put_request(relative_url=relative_url, json=group_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_group_by_realm_by_id(self, realm: str, id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/groups/{id}
        """
        relative_url = f"{api_url}/{realm}/groups/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_children(self, realm: str, id: str, brief_representation: str = None, first: str = None, max: str = None) -> \
    List[GroupRepresentation]:
        """
        Return a paginated list of subgroups that have a parent group corresponding to the group on the URL
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (str): 
            first (str): 
            max (str): 
        
        Returns:
            List[GroupRepresentation]
        
        URL:
            Relative path: /{realm}/groups/{id}/children
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max}
        relative_url = f"{api_url}/{realm}/groups/{id}/children"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [GroupRepresentation.from_dict(item) for item in response.json()]

    def post_children(self, realm: str, id: str, group_representation: GroupRepresentation) -> bool:
        """
        Set or create child.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            group_representation (GroupRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/groups/{id}/children
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/children"
        response = self.api_client.post_request(relative_url=relative_url, json=group_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_group_management_permissions(self, realm: str, id: str) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/groups/{id}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_group_management_permissions(self, realm: str, id: str,
                                         management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/groups/{id}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/groups/{id}/management/permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def get_members(self, realm: str, id: str, brief_representation: bool = None, first: str = None, max: str = None) -> \
    List[UserRepresentation]:
        """
        Get users Returns a stream of users, filtered according to query parameters
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (bool): Only return basic information (only guaranteed to return id, username, created, first and last name, email, enabled state, email verification state, federation link, and access. Note that it means that namely user attributes, required actions, and not before are not returned.)
            first (str): Pagination offset
            max (str): Maximum results size (defaults to 100)
        
        Returns:
            List[UserRepresentation]
        
        URL:
            Relative path: /{realm}/groups/{id}/members
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max}
        relative_url = f"{api_url}/{realm}/groups/{id}/members"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [UserRepresentation.from_dict(item) for item in response.json()]
