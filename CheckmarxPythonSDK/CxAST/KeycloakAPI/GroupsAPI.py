from ..httpRequests import get_request
from ..utilities import get_url_param, type_check
from .Root import api_url


def get_group_hierarchy(realm, brief_representation=False, first=None, max_result_size=100, search=None):
    """

    Args:
        realm:
        brief_representation:
        first:
        max_result_size:
        search:

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
    relative_url = api_url + "/{realm}/users?max={max}".format(realm=realm, max=max)
    relative_url += get_url_param("briefRepresentation", brief_representation)

    relative_url += get_url_param("email", email)
    relative_url += get_url_param("emailVerified", email_verified)
    relative_url += get_url_param("enabled", enabled)
    relative_url += get_url_param("exact", exact)
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    return response