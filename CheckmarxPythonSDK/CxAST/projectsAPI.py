import json
import requests

from .httpRequests import get_request, post_request, put_request, delete_request
from ..compat import NO_CONTENT, OK


def create_a_project(name, groups="", repo_url="", main_branch="", origin="", tags=None, api_version="1.0"):
    """

    Args:
        name (str): The name that you would like to assign to the new Project. The Project name must be unique.
        groups (str, `list` of str): The group IDs of Groups (of users) that you would like to assign to this Project.
                     The ID of a Group can be found using the GET /auth/groups API.
                      A group must already exist in your account before a Project can be assigned to it.
                       Only users assigned to the designated Groups will have access to this Project.
        repo_url (str): The Git repo URL.
        main_branch (str): The Git branch of the source code that is designated as ¡°primary¡± for this Project.
        origin (str): The manner by which the Project was created.
        tags (dict): The tags you want assigned to the Project.
                    Tags need to be formatted in key-value pairs.
                    example:
                    "tags": {"Tag01": "", "Severity": "high"}
        api_version (str):

    Returns:

    """
    relative_url = ""
    if api_version == "1.0":
        relative_url += "/v1"
    relative_url += "/api/projects"

    if isinstance(groups, str):
        groups = [groups]
    elif isinstance(groups, list):
        groups = [str(item) for item in groups]

    data = {
        "name": name,
        "groups": groups,
        "repoUrl": repo_url,
        "mainBranch": main_branch,
        "origin": origin,
        "tags": tags,
    }

    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "groups": item.get("groups"),
        "repoUrl": item.get("repoUrl"),
        "mainBranch": item.get("mainBranch"),
        "origin": item.get("origin"),
        "createdAt": item.get("createdAt"),
        "updatedAt": item.get("updatedAt"),
        "tags": item.get("tags"),
    }


def get_a_list_of_projects():
    pass


def get_project_id_by_name(name):
    """

    Args:
        name (str):

    Returns:
        project_id (str)
    """


def delete_a_project(project_id, api_version="1.0"):
    """

    Args:
        project_id (str):
        api_version (str):
    Returns:

    """
    is_successful = False

    relative_url = ""
    if api_version == "1.0":
        relative_url += "/v1"
    relative_url += "/api/projects/{id}".format(id=project_id)

    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True

    return is_successful
