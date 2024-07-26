# encoding: utf-8
from .httpRequests import get_request, post_request, delete_request
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    Contributors
)

api_url = "/api/contributors"


def get_allowed_and_current_contributors_for_the_current_tenant():
    """

    Returns:

    """
    relative_url = api_url
    response = get_request(relative_url=relative_url)
    item = response.json()
    return Contributors(
        allowed_contributors=item.get("allowedContributors"),
        current_contributors=item.get("currentContributors")
    )


def get_contributors_details_for_current_tenant_exported_in_csv():
    """

    Returns:
        bytes (data of the csv file)
    """
    relative_url = api_url + "/csv"
    response = get_request(relative_url=relative_url)
    return response.content
