from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
import os

from CheckmarxPythonSDK.utilities.compat import OK
from os.path import exists
from requests_toolbelt import MultipartEncoder

api_url = "/api/uploads"


class UploadsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_a_pre_signed_url_to_upload_files(self) -> str:
        """
        Create a pre-signed URL to be used with PUT requests to upload files
         Args:

        Returns:
            url (str)
        """
        url = None
        relative_url = api_url
        response = self.api_client.post_request(relative_url=relative_url, data=None)
        if response.status_code == OK:
            url = response.json().get("url")
        return url

    def upload_zip_content_for_scanning(self, upload_link: str, zip_file_path: str) -> bool:
        """

        Args:
            upload_link (str):
            zip_file_path (str):

        Returns:
            is_successful (bool)
        """
        if not zip_file_path or not exists(zip_file_path):
            print("zip file path: {} does not exist".format(zip_file_path))
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        file_name = os.path.basename(zip_file_path)
        m = MultipartEncoder(
            fields={
                "zippedSource": (file_name, open(zip_file_path, 'rb'), "application/zip")
            }
        )
        headers.update({"Content-Type": m.content_type})
        response = self.api_client.call_api(method="PUT", url=upload_link, data=m, headers=headers)
        return response.status_code == OK


def create_a_pre_signed_url_to_upload_files() -> str:
    return UploadsAPI().create_a_pre_signed_url_to_upload_files()


def upload_zip_content_for_scanning(upload_link: str, zip_file_path: str) -> bool:
    return UploadsAPI().upload_zip_content_for_scanning(upload_link=upload_link, zip_file_path=zip_file_path)
