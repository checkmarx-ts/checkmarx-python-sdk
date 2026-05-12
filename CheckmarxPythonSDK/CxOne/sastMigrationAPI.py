from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from httpx import Response
from .dto import ImportItem, ImportItemWithLogs
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED


class SastMigrationAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/imports"
        )

    def launches_import_from_sast_file(
        self,
        file_name: str,
        encryption_key: str,
        projects_mapping_file_name: str,
    ) -> str:
        """
        Args:
            file_name (str):
            encryption_key (str):
            projects_mapping_file_name (str):

        Returns:
            migration_id (str)
        """
        url = f"{self.base_url}/"
        payload = {
            "fileName": file_name,
            "encryptionKey": encryption_key,
            "projectsMappingFileName": projects_mapping_file_name,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=payload
        )
        if response.status_code == ACCEPTED:
            return response.json().get("migrationId")
        return None

    def get_list_of_imports(self) -> List[ImportItem]:
        """
        Returns:
            List[ImportItem]
        """
        url = f"{self.base_url}/"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return [
                ImportItem.from_dict(item)
                for item in response.json()
            ]
        return None

    def get_info_about_import_by_id(
        self, migration_id: str
    ) -> ImportItemWithLogs:
        """
        Args:
            migration_id (str):

        Returns:
            ImportItemWithLogs
        """
        url = f"{self.base_url}/{migration_id}"
        response = self.api_client.call_api(method="GET", url=url)
        if response.status_code == OK:
            return ImportItemWithLogs.from_dict(response.json())
        return None

    def download_migration_logs(self, migration_id: str) -> Response:
        """
        Args:
            migration_id (str):

        Returns:
            Response
        """
        url = f"{self.base_url}/{migration_id}/logs/download"
        return self.api_client.call_api(method="GET", url=url)


def launches_import_from_sast_file(
    file_name: str,
    encryption_key: str,
    projects_mapping_file_name: str,
) -> str:
    return SastMigrationAPI().launches_import_from_sast_file(
        file_name=file_name,
        encryption_key=encryption_key,
        projects_mapping_file_name=projects_mapping_file_name,
    )


def get_list_of_imports() -> List[ImportItem]:
    return SastMigrationAPI().get_list_of_imports()


def get_info_about_import_by_id(migration_id: str) -> ImportItemWithLogs:
    return SastMigrationAPI().get_info_about_import_by_id(
        migration_id=migration_id
    )


def download_migration_logs(migration_id: str) -> Response:
    return SastMigrationAPI().download_migration_logs(
        migration_id=migration_id
    )
