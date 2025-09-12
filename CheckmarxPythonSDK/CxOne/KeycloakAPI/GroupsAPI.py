import json
from ...utilities.compat import CREATED, NO_CONTENT
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    Group,
    construct_group,
    GroupRepresentation,
    construct_management_permission_reference,
    ManagementPermissionReference,
)
from CheckmarxPythonSDK import (
    logger
)


class GroupsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_group_hierarchy(
            self,
            realm: str,
            brief_representation: bool = False,
            first: int = None,
            max_result_size: int = 100,
            search: str = None
    ) -> List[Group]:
        """
        Get group hierarchy.
        Args:
            realm (str):
            brief_representation (bool):
            first (int):
            max_result_size (int):
            search (str):

        Returns:
            List[Group]
        """
        type_check(realm, str)
        type_check(brief_representation, bool)
        type_check(first, str)
        type_check(max_result_size, int)
        type_check(search, str)

        relative_url = api_url + f"/{realm}/groups"
        params = {"briefRepresentation": brief_representation, "first": first, "max": max_result_size, "search": search}
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True, json=params)
        response = response.json()
        groups = [construct_group(item) for item in response]
        return groups

    def create_group_set(self, realm: str, group_representation: GroupRepresentation) -> bool:
        """
        create or add a top level realm groupSet or create child.
        Args:
            realm (str):
            group_representation (GroupRepresentation):

        Returns:
            bool (True for success, False for failure)
        """
        result = False
        type_check(realm, str)
        type_check(group_representation, GroupRepresentation)
        relative_url = api_url + f"/{realm}/groups"
        post_data = json.dumps(group_representation.to_dict())
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=True)
        if response.status_code == CREATED:
            result = True
        return result

    def get_group_by_name(self, realm: str, group_name: str) -> Group:
        """

        Args:
            realm (str):
            group_name (str):

        Returns:
            Group
        """
        result = None
        type_check(realm, str)
        type_check(group_name, str)
        groups = self.get_group_hierarchy(realm=realm, max_result_size=1000)
        one_group = list(filter(lambda g: g.name == group_name, groups))
        if len(one_group) == 1:
            result = one_group[0]
        return result

    def get_number_of_groups_in_a_realm(self, realm: str) -> int:
        """
        Returns the groups counts.
        Args:
            realm (str):

        Returns:
            int
        """
        type_check(realm, str)
        relative_url = api_url + f"/{realm}/groups/count"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        response = response.json()
        result = response.get("count")
        return result

    def get_group_by_id(self, realm: str, group_id: str) -> Group:
        """

        Args:
            realm (str):
            group_id (str):

        Returns:
            Group
        """
        type_check(realm, str)
        type_check(group_id, str)
        relative_url = api_url + f"/{realm}/groups/{group_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        item = response.json()
        return construct_group(item)

    def update_group_by_id(self, realm: str, group_id: str, group_representation: GroupRepresentation) -> bool:
        """

        Args:
            realm (str):
            group_id (str):
            group_representation (GroupRepresentation):

        Returns:
            bool
        """
        result = False
        type_check(realm, str)
        type_check(group_id, str)
        relative_url = api_url + f"/{realm}/groups/{group_id}"
        type_check(group_representation, GroupRepresentation)
        post_data = json.dumps(group_representation.to_dict())
        response = self.api_client.put_request(relative_url=relative_url, data=post_data, is_iam=True)
        return response.status_code == NO_CONTENT

    def delete_group_by_id(self, realm: str, group_id: str) -> bool:
        """

        Args:
            realm (str):
            group_id (str):

        Returns:

        """
        result = False
        type_check(realm, str)
        type_check(group_id, str)
        relative_url = api_url + f"/{realm}/groups/{group_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == NO_CONTENT

    def create_subgroup(self, realm: str, group_id: str, subgroup_name: str) -> bool:
        """
        Set or create child.
        Args:
            realm (str):
            group_id (str):
            subgroup_name (str):

        Returns:
            bool
        """
        result = False
        type_check(realm, str)
        type_check(group_id, str)
        type_check(subgroup_name, str)
        relative_url = api_url + f"/{realm}/groups/{group_id}/children"
        post_data = json.dumps(
            {
                'name': subgroup_name
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=True)
        return response.status_code == CREATED

    def get_subgroup_by_id(self, realm: str, group_id: str) -> dict:
        """
        Get a subgroup by group id.
        Args:
            realm (str):
            group_id (str):

        Returns:
            dict
        """
        relative_url = f"{api_url}/{realm}/groups/{group_id}/children?max=1000"
        response = self.api_client.get_request(relative_url=relative_url)
        subgroups = response.json()
        return subgroups

    def get_group_permissions(self, realm: str, group_id: str) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have
            been initialized or not and a reference
        Args:
            realm (str):
            group_id (str):

        Returns:
            ManagementPermissionReference
        """
        type_check(realm, str)
        type_check(group_id, str)
        relative_url = api_url + f"/{realm}/groups/{group_id}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        item = response.json()
        return construct_management_permission_reference(item)

    def update_group_permissions(self, realm: str, group_id: str,
                                 group_permissions: ManagementPermissionReference) -> bool:
        """
            Return object stating whether client Authorization permissions have
                been initialized or not and a reference
            Args:
                realm (str):
                group_id (str):
                group_permissions (ManagementPermissionReference):

            Returns:
                ManagementPermissionReference
            """
        type_check(realm, str)
        type_check(group_id, str)
        type_check(group_permissions, ManagementPermissionReference)
        relative_url = api_url + f"/{realm}/groups/{group_id}/management/permissions"
        data = json.dumps(group_permissions.to_dict())
        response = self.api_client.put_request(relative_url=relative_url, data=data, is_iam=True)
        return response.status_code == NO_CONTENT

    def get_group_members(
            self, realm: str, group_id: str, brief_representation: bool = True, first: int = 100,
            max_result_size: int = 100
    ) -> dict:
        """

        Args:
            realm (str):
            group_id (str):
            brief_representation (bool): Only return basic information (only guaranteed to return id, username, created,
                                        first and last name, email, enabled state, email verification state, federation
                                        link, and access. Note that it means that namely user attributes, required actions,
                                        and not before are not returned.)
            first (int): Pagination offset
            max_result_size (int): Maximum results size (defaults to 100)

        Returns:
            List[User]: By doing test, this API only returns empty list
        """

        type_check(realm, str)
        type_check(group_id, str)
        relative_url = api_url + f"/{realm}/groups/{group_id}/members?"
        relative_url += get_url_param("briefRepresentation", brief_representation)
        relative_url += get_url_param("first", first)
        relative_url += get_url_param("max", max_result_size)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        item_list = response.json()
        return item_list

    def create_group(self, realm: str, group_name: str) -> bool:
        """

        Args:
            realm (str):
            group_name (str):

        Returns:
            bool
        """
        result = False
        type_check(realm, str)
        type_check(group_name, str)
        relative_url = api_url + f"/{realm}/groups"
        post_data = json.dumps(
            {
                'name': group_name
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=True)
        return response.status_code == CREATED

    def get_or_create_groups(
            self,
            group_full_name: str,
            realm: str
    ) -> str:
        group = self.get_group_by_name(realm=realm, group_name=group_full_name)
        if group:
            group_id = group.id
            logger.info(f"group {group_full_name} found. Its id is: {group_id}")
            return group_id
        logger.info(f"group {group_full_name} not found. It contains sub groups.")
        group_id = self.create_all_groups(realm=realm, group_full_name=group_full_name)
        logger.info(f"group {group_full_name} created, id: {group_id}")
        return group_id

    def create_all_groups(self, realm: str, group_full_name: str) -> str:
        group_names = group_full_name.split("/")
        root_group_name = group_names[0]
        root_group_id = self.create_root_group_if_not_exist(realm, root_group_name)
        if len(group_names) == 1:
            return root_group_id
        group_id = self.create_sub_groups(
            realm=realm,
            group_names=group_names,
            root_group_id=root_group_id
        )
        return group_id

    def create_sub_groups(self, realm: str, group_names: List[str], root_group_id: str) -> str:
        parent_group_id = root_group_id
        for index, group_name in enumerate(group_names):
            if index == 0:
                continue
            group_path = "/".join(group_names[0: index + 1])
            group = self.get_group_by_name(realm=realm, group_name=group_path)
            if not group:
                logger.info(f"current group: {group_path} does not exist, start create")
                self.create_subgroup(realm=realm, group_id=parent_group_id, subgroup_name=group_name)
                logger.info(f"finish create group: {group_path}")
                group = self.get_group_by_name(realm=realm, group_name=group_path)
            parent_group_id = group.id
        return parent_group_id

    def create_root_group_if_not_exist(self, realm: str, root_group_name: str) -> str:
        root_group = self.get_group_by_name(realm=realm, group_name=root_group_name)
        if root_group:
            root_group_id = root_group.id
            logger.info(f"root group {root_group_name} exist. id: {root_group_id}")
        else:
            logger.info(f"root group not exist, start create root group")
            self.create_group(realm=realm, group_name=root_group_name)
            root_group = self.get_group_by_name(realm=realm, group_name=root_group_name)
            root_group_id = root_group.id
            logger.info(f"root group {root_group_name} created. id: {root_group_id}")
        return root_group_id


def get_group_hierarchy(
            realm: str,
            brief_representation: bool = False,
            first: int = None,
            max_result_size: int = 100,
            search: str = None
    ) -> List[Group]:
    return GroupsAPI().get_group_hierarchy(
        realm=realm, brief_representation=brief_representation, first=first, max_result_size=max_result_size,
        search=search,
    )


def create_group_set(realm: str, group_representation: GroupRepresentation) -> bool:
    return GroupsAPI().create_group_set(realm=realm, group_representation=group_representation)


def get_group_by_name(realm: str, group_name: str) -> Group:
    return GroupsAPI().get_group_by_name(realm=realm, group_name=group_name)


def get_number_of_groups_in_a_realm(realm: str) -> int:
    return GroupsAPI().get_number_of_groups_in_a_realm(realm=realm)


def get_group_by_id(realm: str, group_id: str) -> Group:
    return GroupsAPI().get_group_by_id(realm=realm, group_id=group_id)


def update_group_by_id(realm: str, group_id: str, group_representation: GroupRepresentation) -> bool:
    return GroupsAPI().update_group_by_id(realm=realm, group_id=group_id, group_representation=group_representation)


def delete_group_by_id(realm: str, group_id: str) -> bool:
    return GroupsAPI().delete_group_by_id(realm=realm, group_id=group_id)


def create_subgroup(realm: str, group_id: str, subgroup_name: str) -> bool:
    return GroupsAPI().create_subgroup(realm=realm, group_id=group_id, subgroup_name=subgroup_name)


def get_subgroup_by_id(realm: str, group_id: str) -> dict:
    return GroupsAPI().get_subgroup_by_id(realm=realm, group_id=group_id)


def get_group_permissions(realm: str, group_id: str) -> ManagementPermissionReference:
    return GroupsAPI().get_group_permissions(realm=realm, group_id=group_id)


def update_group_permissions(realm: str, group_id: str, group_permissions: ManagementPermissionReference) -> bool:
    return GroupsAPI().update_group_permissions(realm=realm, group_id=group_id, group_permissions=group_permissions)


def get_group_members(
            realm: str, group_id: str, brief_representation: bool = True, first: int = 100,
            max_result_size: int = 100
    ) -> dict:
    return GroupsAPI().get_group_members(
        realm=realm, group_id=group_id, brief_representation=brief_representation, first=first,
        max_result_size=max_result_size
    )


def create_group(realm: str, group_name: str) -> bool:
    return GroupsAPI().create_group(realm=realm, group_name=group_name)


def get_or_create_groups(
            group_full_name: str,
            realm: str
    ) -> str:
    return GroupsAPI().get_or_create_groups(group_full_name=group_full_name, realm=realm)


def create_all_groups(realm: str, group_full_name: str) -> str:
    return GroupsAPI().create_all_groups(realm=realm, group_full_name=group_full_name)


def create_sub_groups(realm: str, group_names: List[str], root_group_id: str) -> str:
    return GroupsAPI().create_sub_groups(realm=realm, group_names=group_names, root_group_id=root_group_id)


def create_root_group_if_not_exist(realm: str, root_group_name: str) -> str:
    return GroupsAPI().create_root_group_if_not_exist(realm=realm, root_group_name=root_group_name)
