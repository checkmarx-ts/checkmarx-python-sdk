import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url



def add_group_role(realm, group_id, container_id, role_id, role_name):
    type_check(realm, str)
    type_check(group_id, str)
    type_check(role_name, str)
    type_check(role_id, str)

    relative_url = api_url + f"/{realm}/groups/{group_id}/role-mappings/clients/{container_id}"
    post_data = json.dumps(
        [{
            "clientRole": True,
            "composite": True,
            "containerId": f"{container_id}",
            "description": "Scan projects in Groups of this user",
            "id": f"{role_id}",
            "name": f"{role_name}"
        }]
    )
    print(post_data)
    response = post_request(relative_url=relative_url, data=post_data)
    return response