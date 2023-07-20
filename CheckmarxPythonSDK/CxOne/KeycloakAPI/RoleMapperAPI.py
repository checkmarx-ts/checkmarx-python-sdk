import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url


def get_role_mappings(realm, group_id):
    type_check(realm, str)
    type_check(group_id, str)

    relative_url = api_url + f"/{realm}/groups/{group_id}/role-mappings"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response
