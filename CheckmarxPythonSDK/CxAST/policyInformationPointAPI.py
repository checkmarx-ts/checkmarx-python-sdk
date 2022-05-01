from .httpRequests import get_request
from .utilities import get_url_param, type_check
from .dto import Group

access_control_url = "/auth"


def get_groups(group_name=None, limit=None, ids=None):
    """

    Args:
        group_name (str):
        limit (int):
        ids (str):

    Returns:

    """
    type_check(group_name, str)
    type_check(limit, int)
    type_check(ids, str)

    relative_url = access_control_url + "/pip/groups"
    relative_url += get_url_param("groupName", group_name)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("ids", ids)

    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        Group(group_id=item.get("id"), name=item.get("name")) for item in response
    ]
