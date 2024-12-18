import json
from typing import List
from ...utilities.compat import CREATED, OK, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from ..utilities import get_url_param, type_check
from .url import api_url
from .dto import UserRepresentation, construct_user


def get_users(realm, brief_representation=False, email=None, email_verified=None, enabled=None, exact=None, first=None,
              first_name=None, idp_alias=None, idp_user_id=None, last_name=None, max_result_size=1024, search=None,
              username=None):
    """
    Returns a stream of users, filtered according to query parameters

    Args:
        realm (str): realm name (not id!)
        brief_representation (bool): Boolean which defines whether brief representations are returned (default: false)
        email (str): A String contained in email, or the complete email, if param "exact" is true
        email_verified (bool): whether the email has been verified
        enabled (bool): representing if user is enabled or not
        exact (bool): which defines whether the params "last", "first", "email" and "username" must match exactly
        first (int): Pagination offset
        first_name (str): A String contained in firstName, or the complete firstName, if param "exact" is true
        idp_alias (str): The alias of an Identity Provider linked to the user
        idp_user_id (str): The userId at an Identity Provider linked to the user
        last_name (str): A String contained in lastName, or the complete lastName, if param "exact" is true
        max_result_size (int): Maximum results size (defaults to 100)
        search (str): A String contained in username, first or last name, or email
        username (str): A String contained in username, or the complete username, if param "exact" is true

    Returns:
        list of User
    """
    type_check(realm, str)
    type_check(brief_representation, bool)
    type_check(email, str)
    type_check(email_verified, bool)
    type_check(enabled, bool)
    type_check(exact, bool)
    type_check(first, int)
    type_check(first_name, str)
    type_check(idp_alias, str)
    type_check(idp_user_id, str)
    type_check(last_name, str)
    type_check(max_result_size, int)
    type_check(search, str)
    type_check(username, str)

    relative_url = api_url + "/{realm}/users?".format(realm=realm)
    relative_url += get_url_param("briefRepresentation", brief_representation)

    relative_url += get_url_param("email", email)
    relative_url += get_url_param("emailVerified", email_verified)
    relative_url += get_url_param("enabled", enabled)
    relative_url += get_url_param("exact", exact)
    relative_url += get_url_param("first", first)
    relative_url += get_url_param("firstName", first_name)
    relative_url += get_url_param("idpAlias", idp_alias)
    relative_url += get_url_param("idpUserId", idp_user_id)
    relative_url += get_url_param("lastName", last_name)
    relative_url += get_url_param("max", max_result_size)
    relative_url += get_url_param("search", search)
    relative_url += get_url_param("username", username)

    response = get_request(relative_url=relative_url, is_iam=True)
    users = response.json()
    return [construct_user(user) for user in users]


def _filter_user_id_by_name(users, username):
    """

    Args:
        users (list of User):
        username (str):

    Returns:
        str or None
    """
    users_by_name = list(filter(lambda r: r.username == username, users))
    if not users_by_name:
        return None
    user = users_by_name[0]
    user_id = user.id
    return user_id


def get_user_id_by_name(realm, username):
    """

    Args:
        realm (str):
        username (str):

    Returns:
        str
    """
    users = get_users(realm=realm)
    user_id = _filter_user_id_by_name(users, username)
    return user_id


def get_user_id_list_by_username_list(realm: str, username_list: List[str]):
    """

    Args:
        realm (str):
        username_list (list of str):

    Returns:
        list of str
    """
    users = get_users(realm=realm)
    return [_filter_user_id_by_name(users, username) for username in username_list]


def _filter_user_id_by_email(users, email):
    """

    Args:
        users:
        email:

    Returns:

    """
    users_by_email = list(filter(lambda r: r.email == email, users))
    if not users_by_email:
        return None
    user = users_by_email[0]
    user_id = user.id
    return user_id


def get_user_id_by_email(realm, email):
    """

    Args:
        realm (str):
        email (str):

    Returns:
        str
    """
    users = get_users(realm=realm)
    user_id = _filter_user_id_by_email(users, email)
    return user_id


def get_user_id_list_by_email_list(realm, email_list):
    users = get_users(realm=realm)
    return [_filter_user_id_by_email(users, email) for email in email_list]


def create_a_new_user(realm, username, email, first_name, last_name, enabled=True, attributes=None, groups=None,
                      email_verified=False, required_actions=None):
    """
    Username must be unique.
    Args:
        realm (str): realm name (not id!)
        username (str):
        email (str):
        first_name (str):
        last_name (str):
        enabled (bool): user enabled
        attributes (dict): example: {"other":["ccc for test"]}
        groups (list of str):
        email_verified (bool):
        required_actions (list of str): example: ["UPDATE_PASSWORD"]

    Returns:
        bool
    """
    result = False
    relative_url = api_url + "/{realm}/users?".format(realm=realm)
    type_check(username, str)
    type_check(email, str)
    type_check(first_name, str)
    type_check(last_name, str)
    type_check(enabled, bool)
    type_check(attributes, dict)
    type_check(groups, list)
    type_check(email_verified, bool)
    type_check(required_actions, list)
    data = {
        "enabled": enabled,
        "attributes": attributes or {},
        "groups": groups or [],
        "emailVerified": email_verified,
        "username": username,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
    }
    if required_actions:
        data.update({"requiredActions": required_actions or []})
    data = json.dumps(data)
    response = post_request(relative_url=relative_url, data=data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_number_of_users_by_given_criteria(realm, email=None, email_verified=None, enabled=None, first_name=None,
                                          last_name=None, q=None, search=None, username=None):
    """
        Returns the number of users that match the given criteria.
    Args:
        realm (str):  realm name (not id!)
        email (str): email filter
        email_verified (str):
        enabled (str): Boolean representing if user is enabled or not
        first_name (str): first name filter
        last_name (str):
        q (str):
        search (str): arbitrary search string for all the fields below. Default search behavior is prefix-based
                (e.g., foo or foo*). Use foo for infix search and "foo" for exact search.
        username (str): username filter

    Returns:
        int
    """
    relative_url = api_url + f"/{realm}/users/count"
    relative_url += get_url_param("email", email)
    relative_url += get_url_param("emailVerified", email_verified)
    relative_url += get_url_param("enabled", enabled)
    relative_url += get_url_param("firstName", first_name)
    relative_url += get_url_param("lastName", last_name)
    relative_url += get_url_param("q", q)
    relative_url += get_url_param("search", search)
    relative_url += get_url_param("username", username)
    response = get_request(relative_url=relative_url, is_iam=True)
    result = response.json()
    return result


def delete_user(realm, user_id):
    """

    Args:
        realm (str):  realm name (not id!)
        user_id (str):

    Returns:

    """
    result = False
    relative_url = api_url + f"/{realm}/users/{user_id}"
    type_check(realm, str)
    type_check(user_id, str)
    response = delete_request(relative_url=relative_url, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def get_users_profile(realm):
    """

    Args:
        realm (str):

    Returns:

    """
    relative_url = api_url + f"/{realm}/users/profile"
    response = get_request(relative_url=relative_url, is_iam=True)
    return response.json()


def get_users_profile_metadata(realm):
    """

    Args:
        realm:

    Returns:

    """
    relative_url = api_url + f"/{realm}/users/profile/metadata"
    response = get_request(relative_url=relative_url, is_iam=True)
    return response.json()


def get_user_by_id(realm, user_id):
    """

    Args:
        realm (str):
        user_id (str):

    Returns:

    """
    type_check(realm, str)
    type_check(user_id, str)
    relative_url = api_url + f"/{realm}/users/{user_id}"
    response = get_request(relative_url=relative_url, is_iam=True)
    return response.json()


def update_user_by_id(realm, user_id, username, first_name, last_name, email,
                      email_verified=True, user_enabled=True,
                      totp=False, required_actions=None, manage_group_members_ship_access=True, view_access=True,
                      map_roles_access=True, impersonate_access=True, manage_access=True, attributes=None):
    result = False
    relative_url = api_url + f"/{realm}/users/{user_id}"
    data = {
        "username": username, "firstName": first_name, "lastName": last_name, "email": email,
        "emailVerified": email_verified, "enabled": user_enabled, "totp": totp,
        "disableableCredentialTypes": [], "requiredActions": required_actions or [], "notBefore": 0,
        "access": {
            "manageGroupMembership": manage_group_members_ship_access, "view": view_access,
            "mapRoles": map_roles_access, "impersonate": impersonate_access,
            "manage": manage_access
        },
    }
    if attributes:
        data.update({"attributes": attributes})
    data = json.dumps(data)
    response = put_request(relative_url=relative_url, data=data, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result
