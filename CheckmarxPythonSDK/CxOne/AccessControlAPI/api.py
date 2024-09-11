import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url

from .dto import (
    AstIdWithName,
    construct_ast_id_with_name,
    AstUser,
    construct_ast_user,
)

"""
PIP
"""


def get_groups(realm, group_name=None, limit=None, ids=None) -> List[AstIdWithName]:
    """

    Args:
        realm (str):
        group_name (str): Used for searching the groups by name or by part of name.
        limit (int): Max amount of returned record. Applied if groupName param defined.
        ids (str): Ids of groups separated with comma. Has priority over the groupName parameter

    Returns:
        List[AstIdWithName]
    """
    type_check(realm, str)
    type_check(group_name, str)
    type_check(limit, int)
    type_check(ids, str)
    relative_url = api_url + f"/{realm}/pip/groups?"
    relative_url += get_url_param("groupName", group_name)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("ids", ids)
    response = get_request(relative_url=relative_url, is_iam=True)
    item_list = response.json()
    return [construct_ast_id_with_name(item) for item in item_list]


def get_group_by_name(realm, group_name):
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
    groups = get_groups(realm=realm, group_name=group_name)
    one_group = list(filter(lambda g: g.name == group_name, groups))
    if len(one_group) == 1:
        result = one_group[0]
    return result


def get_users(realm, term, limit=100) -> List[AstIdWithName]:
    """

    Args:
        realm (str):
        term (str): required. TODO: check What is term?
        limit (int): Max amount of returned records

    Returns:
        List[AstIdWithName]
    """
    type_check(realm, str)
    type_check(term, str)
    type_check(limit, int)
    relative_url = api_url + f"/{realm}/pip/users?"
    relative_url += get_url_param("term", term)
    relative_url += get_url_param("limit", limit)
    response = get_request(relative_url=relative_url, is_iam=True)
    item_list = response.json()
    return [construct_ast_id_with_name(item) for item in item_list]


def get_users_by_groups(realm, group_id) -> List[AstUser]:
    """

    Args:
        realm (str):
        group_id (str):

    Returns:
        List[AstUser]
    """
    type_check(realm, str)
    type_check(group_id, str)
    relative_url = api_url + f"/{realm}/pip/users/group/{group_id}"
    response = get_request(relative_url=relative_url, is_iam=True)
    item_list = response.json()
    return [construct_ast_user(item) for item in item_list]
