from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
import os

from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT
from typing import List
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

    def start_multipart_upload(self, file_size: int = None) -> dict:
        """
        Create an upload ID for multipart file upload.

        Args:
            file_size (int): Size of the file in bytes.

        Returns:
            dict with uploadID and objectName
        """
        url = f"{self.base_url}/start-multipart-upload"
        body = {"fileSize": file_size} if file_size is not None else {}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def get_multipart_presigned_url(
        self, upload_id: str, part_number: int, object_name: str
    ) -> dict:
        """
        Get a pre-signed URL for uploading a part of a multipart upload.

        Args:
            upload_id (str): The upload ID
            part_number (int): The part number
            object_name (str): The object name

        Returns:
            dict with presignedURL
        """
        url = f"{self.base_url}/multipart-presigned"
        body = {
            "uploadID": upload_id,
            "partNumber": part_number,
            "objectName": object_name,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def complete_multipart_upload(
        self, upload_id: str, object_name: str, part_list: List[dict]
    ) -> bool:
        """
        Complete a multipart upload.

        Args:
            upload_id (str): The upload ID
            object_name (str): The object name
            part_list (List[dict]): List of parts, each with
                eTag (str) and partNumber (int)

        Returns:
            bool
        """
        url = f"{self.base_url}/complete-multipart-upload"
        body = {
            "uploadID": upload_id,
            "objectName": object_name,
            "partList": part_list,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.status_code == NO_CONTENT

    def abort_multipart_upload(
        self, upload_id: str, object_name: str
    ) -> bool:
        """
        Abort a multipart upload.

        Args:
            upload_id (str): The upload ID
            object_name (str): The object name

        Returns:
            bool
        """
        url = f"{self.base_url}/abort-multipart-upload"
        body = {"uploadID": upload_id, "objectName": object_name}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.status_code == NO_CONTENT


def create_a_pre_signed_url_to_upload_files() -> str:
    return UploadsAPI().create_a_pre_signed_url_to_upload_files()


def upload_zip_content_for_scanning(upload_link: str, zip_file_path: str) -> bool:
    return UploadsAPI().upload_zip_content_for_scanning(
        upload_link=upload_link, zip_file_path=zip_file_path
    )


def start_multipart_upload(file_size: int = None) -> dict:
    return UploadsAPI().start_multipart_upload(file_size=file_size)


def get_multipart_presigned_url(
    upload_id: str, part_number: int, object_name: str
) -> dict:
    return UploadsAPI().get_multipart_presigned_url(
        upload_id=upload_id, part_number=part_number, object_name=object_name
    )


def complete_multipart_upload(
    upload_id: str, object_name: str, part_list: List[dict]
) -> bool:
    return UploadsAPI().complete_multipart_upload(
        upload_id=upload_id, object_name=object_name, part_list=part_list
    )


def abort_multipart_upload(upload_id: str, object_name: str) -> bool:
    return UploadsAPI().abort_multipart_upload(
        upload_id=upload_id, object_name=object_name
    )
