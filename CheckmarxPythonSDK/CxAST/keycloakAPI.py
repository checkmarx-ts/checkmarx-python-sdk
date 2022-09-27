from .httpRequests import get_request
from .utilities import get_url_param, type_check

api_url = "/auth/admin/realms"


def get_realms():
    relative_url = api_url
    response = get_request(relative_url=relative_url)
    return response


def get_users(realm, brief_representation=False, email=None, email_verified=None, enabled=None, exact=None, first=None,
              first_name=None, idp_alias=None, idp_user_id=None, last_name=None, max=100, search=None, username=None):
    """

    Args:
        realm (str): realm name (not id!)
        brief_representation (bool): Boolean which defines whether brief representations are returned (default: false)
        email (str): A String contained in email, or the complete email, if param "exact" is true
        email_verified (bool): whether the email has been verified
        enabled (bool): Boolean representing if user is enabled or not
        exact (bool): Boolean which defines whether the params "last", "first", "email" and "username" must match exactly
        first (int): Pagination offset
        first_name (str): A String contained in firstName, or the complete firstName, if param "exact" is true
        idp_alias (str): The alias of an Identity Provider linked to the user
        idp_user_id (str): The userId at an Identity Provider linked to the user
        last_name (str): A String contained in lastName, or the complete lastName, if param "exact" is true
        max (int): Maximum results size (defaults to 100)
        search (str): A String contained in username, first or last name, or email
        username (str): A String contained in username, or the complete username, if param "exact" is true

    Returns:

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
    type_check(max, int)
    type_check(search, str)
    type_check(username, str)

    relative_url = api_url + "/{realm}/users?max={max}".format(realm=realm, max=max)
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
    relative_url += get_url_param("max", max)
    relative_url += get_url_param("search", search)
    relative_url += get_url_param("username", username)

    response = get_request(relative_url=relative_url)
    response = response.json()
    return response
