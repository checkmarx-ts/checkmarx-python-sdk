import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url
from .dto import RoleRepresentation


def get_all_roles_for_the_client(realm: str, client_id: str,
                                 brief_representation: bool = False,
                                 first: int = None,
                                 max: int = None,
                                 search: bool = None):
    """

    Args:
        realm (str):
        client_id (str):
        brief_representation (bool):
        first (int):
        max (int):
        search (bool):

    Returns:
        dict
    """
    type_check(realm, str)
    type_check(client_id, str)
    type_check(brief_representation, bool)
    type_check(first, int)
    type_check(max, int)
    relative_url = api_url + f"/{realm}/clients/{client_id}/roles?"
    relative_url += get_url_param("briefRepresentation", brief_representation)
    relative_url += get_url_param("first", first)
    relative_url += get_url_param("max", max)
    relative_url += get_url_param("search", search)
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response


def create_role_for_the_client(realm: str, client_id: str, role_name: str, description: str = None):
    """

    Args:
        realm (str):
        client_id (str):
        role_name (str):
        description (str):

    Returns:
        bool
    """
    is_successful = False
    type_check(realm, str)
    type_check(client_id, str)
    type_check(role_name, str)
    relative_url = api_url + f"/{realm}/clients/{client_id}/roles"
    data = json.dumps({
        "name": role_name,
        "description": description,
        "composite": True,
        "clientRole": True,
        "attributes": {
            "category": ["Composite role"],
            "type": ["Role"],
        }
    })
    response = post_request(relative_url=relative_url, data=data, is_iam=True)
    if response.status_code == CREATED:
        is_successful = True
    return is_successful


def delete_role_by_name(realm: str, client_id: str, role_name: str):
    is_successful = False
    type_check(realm, str)
    type_check(client_id, str)
    type_check(role_name, str)
    relative_url = api_url + f"/{realm}/clients/{client_id}/roles/{role_name}"
    response = delete_request(relative_url=relative_url, is_iam=True)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def get_role_by_name(realm: str, client_id: str, role_name: str):
    """

    Args:
        realm:
        client_id:
        role_name:

    Returns:
        dict
        example
        {
            "id": "35334ef1-989c-4c08-aaf9-3c4e2c4e6e9e",
            "name": "test111111111",
            "composite": false,
            "clientRole": true,
            "containerId": "d3b60524-13a1-431a-a703-1d6d3d09f512",
            "attributes": {
                "creator": [
                    "happy_yang"
                ],
                "lastUpdate": [
                    "1737608480336"
                ]
            }
        }
    """
    type_check(realm, str)
    type_check(client_id, str)
    type_check(role_name, str)
    relative_url = api_url + f"/{realm}/clients/{client_id}/roles/{role_name}"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response


def update_role_by_id(realm: str, role_id: str, role_representation: RoleRepresentation):
    """

    Args:
        realm (str):
        role_id (str):
        role_representation (RoleRepresentation):
            {"attributes": {"type": ["Role"], "category": ["Composite role"], "creator": ["happy_yang"],
                        "lastUpdate": ["1737608480336"]}, "clientRole": true, "composite": true,
         "containerId": "d3b60524-13a1-431a-a703-1d6d3d09f512", "id": "35334ef1-989c-4c08-aaf9-3c4e2c4e6e9e",
         "name": "test111111111"}
    Returns:
        bool
    """
    is_successful = False
    relative_url = api_url + f"/{realm}/roles-by-id/{role_id}"
    data = json.dumps(role_representation.to_dict())
    response = put_request(relative_url=relative_url, data=data, is_iam=True)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def get_roles_children(realm: str, role_id: str):
    """
        Get role’s children Returns a set of role’s children provided the role is a composite.
    Args:
        realm:
        role_id:

    Returns:
        dict
    """
    relative_url = api_url + f"/{realm}/roles-by-id/{role_id}/composites"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response


def get_roles_children_iam(realm: str, role_id: str):
    """

    Args:
        realm:
        role_id:

    Returns:

    """
    relative_url = api_url + f"/{realm}/roles-by-id/{role_id}/composites/realm"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response


def add_children_to_a_composite_role(realm: str, role_id: str, children: List[RoleRepresentation]):
    """

    Args:
        realm (str):
        role_id (str):
        children (str): [{"clientRole": true, "composite": true, "containerId": "d3b60524-13a1-431a-a703-1d6d3d09f512",
          "description": "Scan, manage results, manage projects", "id": "260f1dba-9ac4-451d-bd9f-4f2249e0ae7d",
          "name": "ast-scanner"}]

    Returns:
        bool
    """
    is_successful = False
    relative_url = api_url + f"/{realm}/roles-by-id/{role_id}/composites"
    data = json.dumps([role_representation.to_dict() for role_representation in children])
    response = post_request(relative_url=relative_url, data=data, is_iam=True)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def get_all_roles_for_the_realm(realm):
    type_check(realm, str)
    relative_url = api_url + f"/{realm}/roles"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response
