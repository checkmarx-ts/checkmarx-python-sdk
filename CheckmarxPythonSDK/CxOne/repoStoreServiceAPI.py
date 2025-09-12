from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
import json
from .dto import FileInfo, construct_file_info
from CheckmarxPythonSDK.utilities.compat import OK

repo_store_url = "/api/repostore"


def construct_list_of_file_info(response):
    response = response.json()
    return [
        FileInfo(
            name=item.get("name"),
            mod_time=item.get("modTime"),
            size=item.get("size"),
            is_dir=item.get("isDir"),
        )
        for item in response or []]


class RepoStoreServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def check_if_scan_has_source_code_available(self, scan_id: str) -> bool:
        """

        Args:
            scan_id (str):

        Returns:
            bool
        """
        relative_url = repo_store_url + f"/scans/{scan_id}"
        response = self.api_client.head_request(relative_url=relative_url)
        return response.status_code == OK

    def download_source_code_from_specific_scan(self, scan_id: str) -> bytes:
        """

        Args:
            scan_id (str):

        Returns:
            bytes
        """
        relative_url = repo_store_url + f"/code/{scan_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.status_code == OK

    def view_scanned_source_files(self, scan_id: str) -> List[FileInfo]:
        """

        Args:
            scan_id (str):

        Returns:
            List[FileInfo]
        """
        relative_url = repo_store_url + f"/files/{scan_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return [construct_file_info(file_info) for file_info in item]

    def view_scanned_source_files_in_specified_folder(self, scan_id: str, folder: str) -> List[FileInfo]:
        """

        Args:
            scan_id (str):
            folder (str):

        Returns:
            List[FileInfo]
        """
        relative_url = repo_store_url + f"/files/{scan_id}/{folder}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return [construct_file_info(file_info) for file_info in item]

    def view_source_code_of_specified_file(self, scan_id: str, file_name: str) -> bool:
        """

        Args:
            scan_id (str):
            file_name (str):

        Returns:
            bool
        """
        relative_url = repo_store_url + f"/files/{scan_id}/{file_name}"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.status_code == 308

    def get_the_list_of_branches_inside_a_git_repository(
            self, project_id: str, repo_url: str, token: str = None, ssh_key: str = None
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
        result = None
        relative_url = repo_store_url + "/git/fetch-branches"
        data = json.dumps(
            {
                "repoURL": repo_url,
                "token": token,
                "projectID": project_id,
                "sshKey": ssh_key
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result


def check_if_scan_has_source_code_available(scan_id: str) -> bool:
    return RepoStoreServiceAPI().check_if_scan_has_source_code_available(scan_id=scan_id)


def download_source_code_from_specific_scan(scan_id: str) -> bytes:
    return RepoStoreServiceAPI().download_source_code_from_specific_scan(scan_id=scan_id)


def view_scanned_source_files(scan_id: str) -> List[FileInfo]:
    return RepoStoreServiceAPI().view_scanned_source_files(scan_id=scan_id)


def view_scanned_source_files_in_specified_folder(scan_id: str, folder: str) -> List[FileInfo]:
    return RepoStoreServiceAPI().view_scanned_source_files_in_specified_folder(scan_id=scan_id, folder=folder)


def view_source_code_of_specified_file(scan_id: str, file_name: str) -> bool:
    return RepoStoreServiceAPI().view_source_code_of_specified_file(scan_id=scan_id, file_name=file_name)


def get_the_list_of_branches_inside_a_git_repository(
        project_id: str, repo_url: str, token: str = None, ssh_key: str = None
) -> List[str]:
    return RepoStoreServiceAPI().get_the_list_of_branches_inside_a_git_repository(
        project_id=project_id, repo_url=repo_url, token=token, ssh_key=ssh_key
    )
