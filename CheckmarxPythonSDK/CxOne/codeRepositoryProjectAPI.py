# encoding: utf-
import json
from .httpRequests import get_request, post_request, delete_request
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import SCMImportInput

api_url = "/api/repos-manager"


def import_code_repository(scm_import_input: SCMImportInput):
    """

    Args:
        scm_import_input (SCMImportInput):

    Returns:
        processId
            string
            The unique identifier of this conversion process. You will use this ID with the
            GET conversion/status/{process_id} API to check the status of the conversion.

        message
            string
            A message that includes the url for checking the conversion status.
    """
    type_check(scm_import_input, SCMImportInput)
    relative_url = api_url + "/scm-projects"
    response = post_request(relative_url=relative_url, data=json.dumps(scm_import_input.to_dict()))
    return response.json()


def retrieve_import_status(process_id: str):
    """

    Args:
        process_id: The unique identifier of the import process for which you would like to check the status

    Returns:

    """
    type_check(process_id, str)
    relative_url = api_url + f"/scm-projects/import-status?process-id={process_id}"
    response = get_request(relative_url=relative_url)
    return response.json()
