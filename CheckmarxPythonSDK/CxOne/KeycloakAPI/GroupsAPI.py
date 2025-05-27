import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
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


def get_group_hierarchy(realm, brief_representation=False, first=None, max_result_size=100, search=None) -> List[Group]:
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

    relative_url = api_url + f"/{realm}/groups?"
    relative_url += get_url_param("briefRepresentation", brief_representation)
    relative_url += get_url_param("first", first)
    relative_url += get_url_param("max", max_result_size)
    relative_url += get_url_param("search", search)
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    groups = [construct_group(item) for item in response]
    return groups


def create_group_set(realm, group_representation) -> bool:
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
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_group_by_name(realm, group_name) -> Group:
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
    groups = get_group_hierarchy(realm=realm, max_result_size=1000)
    one_group = list(filter(lambda g: g.name == group_name, groups))
    if len(one_group) == 1:
        result = one_group[0]
    return result


def get_number_of_groups_in_a_realm(realm) -> int:
    """
    Returns the groups counts.
    Args:
        realm (str):

    Returns:
        int
    """
    type_check(realm, str)
    relative_url = api_url + f"/{realm}/groups/count"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    result = response.get("count")
    return result


def get_group_by_id(realm, group_id) -> Group:
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
    response = get_request(relative_url=relative_url, is_iam=True)
    item = response.json()
    return construct_group(item)


def update_group_by_id(realm, group_id, group_representation) -> bool:
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
    response = put_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def delete_group_by_id(realm, group_id) -> bool:
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
    response = delete_request(relative_url=relative_url, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def create_subgroup(realm, group_id, subgroup_name) -> bool:
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
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_subgroup_by_id(realm, group_id):
    """
    Get a subgroup by group id.
    Args:
        realm (str):
        group_id (str):

    Returns:
        bool
    """
    relative_url = f"{api_url}/{realm}/groups/{group_id}/children?max=1000"
    response = get_request(relative_url=relative_url)
    subgroups = response.json()
    return subgroups


def get_group_permissions(realm, group_id) -> ManagementPermissionReference:
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
    response = get_request(relative_url=relative_url, is_iam=True)
    item = response.json()
    return construct_management_permission_reference(item)


def update_group_permissions(realm, group_id, group_permissions):
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
    result = False
    type_check(realm, str)
    type_check(group_id, str)
    type_check(group_permissions, ManagementPermissionReference)
    relative_url = api_url + f"/{realm}/groups/{group_id}/management/permissions"
    data = json.dumps(group_permissions.to_dict())
    response = put_request(relative_url=relative_url, data=data, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def get_group_members(realm, group_id, brief_representation=True, first=100, max_result_size=100):
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
    response = get_request(relative_url=relative_url, is_iam=True)
    item_list = response.json()
    return item_list


def create_group(realm, group_name):
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
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_or_create_groups(
        group_full_name: str,
        realm: str
) -> str:
    group = get_group_by_name(realm=realm, group_name=group_full_name)
    if group:
        group_id = group.id
        logger.info(f"group {group_full_name} found. Its id is: {group_id}")
        return group_id
    logger.info(f"group {group_full_name} not found. It contains sub groups.")
    group_id = create_all_groups(realm=realm, group_full_name=group_full_name)
    logger.info(f"group {group_full_name} created, id: {group_id}")
    return group_id


def create_all_groups(realm, group_full_name) -> str:
    group_names = group_full_name.split("/")
    root_group_name = group_names[0]
    root_group_id = create_root_group_if_not_exist(realm, root_group_name)
    if len(group_names) == 1:
        return root_group_id
    group_id = create_sub_groups(
        realm=realm,
        group_names=group_names,
        root_group_id=root_group_id
    )
    return group_id


def create_sub_groups(realm, group_names, root_group_id) -> str:
    parent_group_id = root_group_id
    for index, group_name in enumerate(group_names):
        if index == 0:
            continue
        group_path = "/".join(group_names[0: index + 1])
        group = get_group_by_name(realm=realm, group_name=group_path)
        if not group:
            logger.info(f"current group: {group_path} does not exist, start create")
            create_subgroup(realm=realm, group_id=parent_group_id, subgroup_name=group_name)
            logger.info(f"finish create group: {group_path}")
            group = get_group_by_name(realm=realm, group_name=group_path)
        parent_group_id = group.id
    return parent_group_id


def create_root_group_if_not_exist(realm, root_group_name) -> str:
    root_group = get_group_by_name(realm=realm, group_name=root_group_name)
    if root_group:
        root_group_id = root_group.id
        logger.info(f"root group {root_group_name} exist. id: {root_group_id}")
    else:
        logger.info(f"root group not exist, start create root group")
        create_group(realm=realm, group_name=root_group_name)
        root_group = get_group_by_name(realm=realm, group_name=root_group_name)
        root_group_id = root_group.id
        logger.info(f"root group {root_group_name} created. id: {root_group_id}")
    return root_group_id
