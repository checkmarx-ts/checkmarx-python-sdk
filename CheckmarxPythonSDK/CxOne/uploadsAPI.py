# encoding: utf-8
import requests
import os

from .httpRequests import post_request
from CheckmarxPythonSDK.utilities.compat import OK
from os.path import exists
from CheckmarxPythonSDK.utilities.httpRequests import auth_header
from requests_toolbelt import MultipartEncoder

api_url = "/api/uploads"


def create_a_pre_signed_url_to_upload_files():
    """
    Create a pre-signed URL to be used with PUT requests to upload files

    Args:

    Returns:
        url (str)
    """
    url = None
    relative_url = api_url
    response = post_request(relative_url=relative_url, data=None)
    if response.status_code == OK:
        url = response.json().get("url")
    return url


def upload_zip_content_for_scanning(upload_link, zip_file_path):
    """

    Args:
        upload_link (str):
        zip_file_path (str):

    Returns:
        is_successful (bool)
    """
    is_successful = False

    if not zip_file_path or not exists(zip_file_path):
        print("zip file path: {} does not exist".format(zip_file_path))

    url = "{uploadLink}".format(uploadLink=upload_link)

    headers = auth_header.copy()
    headers.update(
        {"Content-Type": "application/x-www-form-urlencoded"}
    )
    file_name = os.path.basename(zip_file_path)
    m = MultipartEncoder(
        fields={
            "zippedSource": (file_name, open(zip_file_path, 'rb'), "application/zip")
        }
    )
    headers.update({"Content-Type": m.content_type})
    # with open(zip_file_path, 'rb') as data:
    response = requests.put(url=url, data=m, headers=headers, verify=False)
    if response.status_code == OK:
        is_successful = True

    return is_successful
