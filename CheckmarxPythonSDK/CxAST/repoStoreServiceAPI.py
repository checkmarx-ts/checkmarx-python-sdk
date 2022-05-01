from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import Tree, FileInfo

repo_store_url = "/api/repostore"


def __construct_list_of_file_info(response):
    response = response.json()
    return [
        FileInfo(
            name=item.get("name"),
            mod_time=item.get("modTime"),
            size=item.get("size"),
            is_dir=item.get("isDir"),
        )
        for item in response or []]


def get_commit_content(commit_id):
    """

    Args:
        commit_id (str):

    Returns:
        list of FileInfo
    """
    relative_url = repo_store_url + "/files/{commit_id}".format(commit_id=commit_id)
    response = get_request(relative_url=relative_url)
    return __construct_list_of_file_info(response)


def get_folder_content(commit_id, folder):
    """

    Args:
        commit_id (str):
        folder (str):

    Returns:
        list of FileInfo
    """
    relative_url = repo_store_url + "/files/{commit_id}/{folder}".format(commit_id=commit_id, folder=folder)
    response = get_request(relative_url=relative_url)
    return __construct_list_of_file_info(response)


def get_code(commit_id, file_name):
    """

    Args:
        commit_id (str):
        file_name (str):

    Returns:

    """
    relative_url = repo_store_url + "/files/{commit_id}/{file_name}".format(commit_id=commit_id, file_name=file_name)
    response = get_request(relative_url=relative_url)
    return response


def get_project_tree_structure(commit_id):
    """

    Args:
        commit_id (str):

    Returns:

    """
    relative_url = repo_store_url + "/files/{commit_id}/{file_name}".format(commit_id=commit_id, file_name=file_name)
    response = get_request(relative_url=relative_url)
    return response


def get_the_list_of_branches_inside_a_git_repository(project_id, repo_url, token=None):
    relative_url = repo_store_url + "/git/fetch-branches?project-id={project_id}&repo-url={repo_url}".format(
        project_id=project_id, repo_url=repo_url
    )
    relative_url += get_url_param("token", token)
    response = get_request(relative_url=relative_url)
    return response
