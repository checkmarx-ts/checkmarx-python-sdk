from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from requests import Response
import json
from .dto import (
    ImportItem, construct_import_item,
    ImportItemWithLogs, construct_import_item_with_logs,
)
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED

api_url = "/api/imports"


class SastMigrationAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def launches_import_from_sast_file(
            self, file_name: str, encryption_key: str, projects_mapping_file_name: str
    ) -> str:
        """

        Args:
            file_name (str):
            encryption_key (str):
            projects_mapping_file_name (str):

        Returns:
            migration_id (str)
        """
        result = None
        relative_url = api_url + "/"
        data = json.dumps(
            {
                "fileName": file_name,
                "encryptionKey": encryption_key,
                "projectsMappingFileName": projects_mapping_file_name
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=data)
        if response.status_code == ACCEPTED:
            response = response.json()
            result = response.get("migrationId")
        return result

    def get_list_of_imports(self) -> List[ImportItem]:
        """

        Returns:
            List[ImportItem]
        """
        result = None
        relative_url = api_url + "/"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            response = response.json()
            result = [
                construct_import_item(item) for item in response
            ]
        return result

    def get_info_about_import_by_id(self, migration_id: str) -> ImportItemWithLogs:
        """

        Args:
            migration_id (str):

        Returns:
            ImportItemWithLogs
        """
        result = None
        relative_url = api_url + f"/{migration_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        if response.status_code == OK:
            response = response.json()
            result = construct_import_item_with_logs(response)
        return result

    def download_migration_logs(self, migration_id: str) -> Response:
        """

        Args:
            migration_id (str):

        Returns:
            Response
        """
        relative_url = api_url + f"/{migration_id}/logs/download"
        response = self.api_client.get_request(relative_url=relative_url)
        return response


def launches_import_from_sast_file(file_name: str, encryption_key: str, projects_mapping_file_name: str) -> str:
    return SastMigrationAPI().launches_import_from_sast_file(
        file_name=file_name, encryption_key=encryption_key, projects_mapping_file_name=projects_mapping_file_name
    )


def get_list_of_imports() -> List[ImportItem]:
    return SastMigrationAPI().get_list_of_imports()


def get_info_about_import_by_id(migration_id: str) -> ImportItemWithLogs:
    return SastMigrationAPI().get_info_about_import_by_id(migration_id=migration_id)


def download_migration_logs(migration_id: str) -> Response:
    return SastMigrationAPI().download_migration_logs(migration_id=migration_id)
