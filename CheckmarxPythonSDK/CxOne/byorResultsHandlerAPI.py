# encoding: utf-8
import json
from .httpRequests import post_request
from .utilities import type_check
from .dto import (
    ImportRequest,
    ImportResults,
)

api_url = "/api/byor"


def create_byor_import(import_request):
    """

    Args:
        import_request (ImportRequest):

    Returns:
        ImportResults
    """
    type_check(import_request, ImportRequest)
    relative_url = api_url + "/imports"
    data = json.dumps(import_request.to_dict())
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return ImportResults(import_id=item.get("importId"))
