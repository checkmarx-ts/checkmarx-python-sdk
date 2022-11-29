from ...utilities.compat import CREATED
from ..httpRequests import get_request, post_request, put_request, delete_request

import json
from ..httpRequests import get_request
from ..utilities import get_url_param, type_check
from .url import api_url

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    Group,
    construct_group,
    GroupRepresentation,
)


def get_group_hierarchy(realm, brief_representation=False, first=None, max_result_size=100, search=None):
    """

    Args:
        realm (str):
        brief_representation (bool):
        first (int):
        max_result_size (int):
        search (str):

    Returns:
        list of Group
    """
    type_check(realm, str)
    type_check(brief_representation, bool)
    type_check(first, str)
    type_check(max_result_size, int)
    type_check(search, str)

    relative_url = api_url + f"/{realm}/groups"
    relative_url += "?"
    relative_url += get_url_param("briefRepresentation", brief_representation)
    relative_url += get_url_param("first", first)
    relative_url += get_url_param("max", max_result_size)
    relative_url += get_url_param("search", search)
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    groups = [construct_group(item) for item in response]
    return groups


def create_group_set(realm, group_representation):
    """

    Args:
        realm:
        group_representation:

    Returns:
        bool (True for success, False for failure)
    """
    result = False
    type_check(realm, str)
    type_check(group_representation, GroupRepresentation)
    relative_url = api_url + f"/{realm}/groups"
    post_data = group_representation.get_post_data()
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_group_by_name(realm, group_name):
    type_check(realm, str)
    type_check(group_name, str)

    relative_url = api_url + f"/{realm}/groups"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    groups = [construct_group(item) for item in response]

    for group in groups:
        if group_name and group.name == group_name:
            return group.id


def create_group(realm, group_name):
    type_check(realm, str)

    relative_url = api_url + f"/{realm}/groups"
    post_data = json.dumps(
        {
            'name': group_name 
        }
    )
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    return response


def create_subgroup(realm, group_id, subgroup_name):
    type_check(realm, str)

    relative_url = api_url + f"/{realm}/groups/{group_id}/children"
    post_data = json.dumps(
        {
            'name': subgroup_name 
        }
    )
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    return response


def add_group_role(realm, group_id, container_id, role_id, role_name):
    type_check(realm, str)
    type_check(group_id, str)
    type_check(role_name, str)
    type_check(role_id, str)

    relative_url = api_url + f"/{realm}/groups/{group_id}/role-mappings/clients/{container_id}" 
    post_data = json.dumps(
        [{
            "clientRole": True,
            "composite":True,
            "containerId":f"{container_id}",
            "description":"Scan projects in Groups of this user",
            "id":f"{role_id}",
            "name":f"{role_name}"
        }]
    )
    print(post_data)
    response = post_request(relative_url=relative_url, data=post_data)
    return response

