from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
import os

from CheckmarxPythonSDK.utilities.compat import OK
from os.path import exists


class UploadsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/uploads"
        )

    def create_a_pre_signed_url_to_upload_files(self) -> str:
        """
        Create a pre-signed URL to be used with PUT requests to upload files.

        Returns:
            url (str)
        """
        url = None
        response = self.api_client.call_api(
            method="POST", url=self.base_url
        )
        if response.status_code == OK:
            url = response.json().get("url")
        return url

    def upload_zip_content_for_scanning(
        self, upload_link: str, zip_file_path: str
    ) -> bool:
        """

        Args:
            upload_link (str):
            zip_file_path (str):

        Returns:
            is_successful (bool)
        """
        if not zip_file_path or not exists(zip_file_path):
            print("zip file path: {} does not exist".format(zip_file_path))
        file_name = os.path.basename(zip_file_path)
        response = self.api_client.call_api(
            method="PUT",
            url=upload_link,
            files={
                "zippedSource": (
                    file_name,
                    open(zip_file_path, "rb"),
                    "application/zip",
                )
            },
        )
        return response.status_code == OK


def create_a_pre_signed_url_to_upload_files() -> str:
    return UploadsAPI().create_a_pre_signed_url_to_upload_files()


def upload_zip_content_for_scanning(upload_link: str, zip_file_path: str) -> bool:
    return UploadsAPI().upload_zip_content_for_scanning(
        upload_link=upload_link, zip_file_path=zip_file_path
    )
