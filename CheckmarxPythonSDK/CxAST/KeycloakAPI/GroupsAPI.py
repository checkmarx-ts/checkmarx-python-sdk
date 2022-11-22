from ..httpRequests import get_request
from ..utilities import get_url_param, type_check
from .url import api_url

from CheckmarxPythonSDK.CxAST.KeycloakAPI.dto import (
    Group,
    construct_group,
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

