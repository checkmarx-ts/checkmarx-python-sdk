import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url

from .dto import (
    AstIdWithName,
    construct_ast_id_with_name,
)

# PIP


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
    if group_name:
        relative_url += f"groupName={group_name}"
    if limit:
        relative_url += f"&limit={limit}"
    if ids:
        relative_url += f"&ids={ids}"
    response = get_request(relative_url=relative_url, is_iam=True)
    item_list = response.json()
    return [construct_ast_id_with_name(item) for item in item_list]
