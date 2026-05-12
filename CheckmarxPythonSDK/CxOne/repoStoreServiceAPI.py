from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import FileInfo
from CheckmarxPythonSDK.utilities.compat import OK


class RepoStoreServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/repostore"
        )

    def check_if_scan_has_source_code_available(
        self, scan_id: str
    ) -> bool:
        """
        Args:
            scan_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/scans/{scan_id}"
        response = self.api_client.call_api(method="HEAD", url=url)
        return response.status_code == OK

    def download_source_code_from_specific_scan(
        self, scan_id: str
    ) -> bytes:
        """
        Args:
            scan_id (str):

        Returns:
            bytes
        """
        url = f"{self.base_url}/code/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.status_code == OK

    def view_scanned_source_files(
        self, scan_id: str
    ) -> List[FileInfo]:
        """
        Args:
            scan_id (str):

        Returns:
            List[FileInfo]
        """
        url = f"{self.base_url}/files/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            FileInfo.from_dict(file_info)
            for file_info in (response.json() or [])
        ]

    def view_scanned_source_files_in_specified_folder(
        self, scan_id: str, folder: str
    ) -> List[FileInfo]:
        """
        Args:
            scan_id (str):
            folder (str):

        Returns:
            List[FileInfo]
        """
        url = f"{self.base_url}/files/{scan_id}/{folder}"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            FileInfo.from_dict(file_info)
            for file_info in (response.json() or [])
        ]

    def view_source_code_of_specified_file(
        self, scan_id: str, file_path: str
    ) -> str:
        """
        Args:
            scan_id (str):
            file_path (str):

        Returns:
            str
        """
        url = f"{self.base_url}/files/{scan_id}/{file_path}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.text

    def get_the_list_of_branches_inside_a_git_repository(
        self,
        project_id: str,
        repo_url: str,
        token: str = None,
        ssh_key: str = None,
    ) -> List[str]:
        """
        Args:
            project_id (str):
            repo_url (str):
            token (str):
            ssh_key (str):

        Returns:
            List[str]
        """
        url = f"{self.base_url}/git/fetch-branches"
        payload = {
            "repoURL": repo_url,
            "token": token,
            "projectID": project_id,
            "sshKey": ssh_key,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=payload
        )
        if response.status_code == OK:
            return response.json()
        return None


def check_if_scan_has_source_code_available(scan_id: str) -> bool:
    return RepoStoreServiceAPI().check_if_scan_has_source_code_available(
        scan_id=scan_id
    )


def download_source_code_from_specific_scan(scan_id: str) -> bytes:
    return RepoStoreServiceAPI().download_source_code_from_specific_scan(
        scan_id=scan_id
    )


def view_scanned_source_files(scan_id: str) -> List[FileInfo]:
    return RepoStoreServiceAPI().view_scanned_source_files(
        scan_id=scan_id
    )


def view_scanned_source_files_in_specified_folder(
    scan_id: str, folder: str
) -> List[FileInfo]:
    return RepoStoreServiceAPI().view_scanned_source_files_in_specified_folder(
        scan_id=scan_id, folder=folder
    )


def view_source_code_of_specified_file(
    scan_id: str, file_path: str
) -> str:
    return RepoStoreServiceAPI().view_source_code_of_specified_file(
        scan_id=scan_id, file_path=file_path
    )


def get_the_list_of_branches_inside_a_git_repository(
    project_id: str,
    repo_url: str,
    token: str = None,
    ssh_key: str = None,
) -> List[str]:
    return RepoStoreServiceAPI().get_the_list_of_branches_inside_a_git_repository(
        project_id=project_id,
        repo_url=repo_url,
        token=token,
        ssh_key=ssh_key,
    )
