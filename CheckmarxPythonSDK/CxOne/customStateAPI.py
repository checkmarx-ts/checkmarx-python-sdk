# encoding: utf-8
from .httpRequests import get_request, post_request, delete_request

api_url = "/api/custom-states"


def get_all_custom_states(include_deleted: bool = False):
    """

    Args:
        include_deleted:

    Returns:
        [
          {
            "id": 391,
            "name": "demo1",
            "type": "INFO",
            "isAllowed": true
          },
          {
            "id": 390,
            "name": "demo2",
            "type": "INFO",
            "isAllowed": false
          }
        ]
    """
    relative_url = api_url + f"?include-deleted={include_deleted}"
    response = get_request(relative_url=relative_url)
    item = response.json()
    return item


def create_a_custom_state(name: str):
    response = post_request(relative_url=api_url, json={"name": name})
    return response


def delete_a_custom_state(id: str):
    relative_url = api_url + f"/{id}"
    response = delete_request(relative_url=relative_url)
    return response
