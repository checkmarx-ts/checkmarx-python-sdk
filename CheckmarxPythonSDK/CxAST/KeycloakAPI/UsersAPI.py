from ...utilities.compat import CREATED
from ..httpRequests import get_request, post_request, put_request, delete_request
from ..utilities import get_url_param, type_check
from .url import api_url
from .dto import UserRepresentation, construct_user


def get_users(realm, brief_representation=False, email=None, email_verified=None, enabled=None, exact=None, first=None,
              first_name=None, idp_alias=None, idp_user_id=None, last_name=None, max_result_size=100, search=None,
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


def create_a_new_user(realm, user_representation):
    """
    Username must be unique.
    Args:
        realm (str): realm name (not id!)
        user_representation (UserRepresentation):

    Returns:
        bool
    """
    result = False
    relative_url = api_url + "/{realm}/users?".format(realm=realm)
    type_check(user_representation, UserRepresentation)
    post_data = user_representation.get_post_data()
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result
