# encoding: utf-8
import json

from .httpRequests import post_request
from ..compat import OK


def create_a_pre_signed_url_to_upload_files():
    """
    Create a pre-signed URL to be used with PUT requests to upload files

    Args:

    Returns:
        url (str)
    """
    url = None
    relative_url = "/api/uploads"
    response = post_request(relative_url=relative_url, data=None)
    if response.status_code == OK:
        url = response.json().get("url")
    return url

