from ..httpRequests import get_request
from .url import api_url
from .dto import construct_realm_representation


def get_realms():
    """

    Returns:
        list of RealmRepresentation
    """
    relative_url = api_url
    response = get_request(relative_url=relative_url, is_iam=True)
    realms = response.json()
    return [construct_realm_representation(realm) for realm in realms]
