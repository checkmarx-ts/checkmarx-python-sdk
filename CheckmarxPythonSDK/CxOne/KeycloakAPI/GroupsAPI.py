from ...utilities.compat import CREATED
from ..httpRequests import get_request, post_request, put_request, delete_request
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
