# encoding: utf-8
from .httpRequests import get_request, post_request, put_request, delete_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    ImportRequest,
    ImportResults,
)


def create_byor_import(import_request):
    """

    Args:
        import_request (ImportRequest):

    Returns:
        ImportResults
    """
    type_check(import_request, ImportRequest)
    relative_url = "/api/byor/imports"
    data = import_request.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return ImportResults(import_id=item.get("importId"))
