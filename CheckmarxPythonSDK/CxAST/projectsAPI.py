# encoding: utf-8
import json
import requests

from .httpRequests import get_request, post_request, put_request, delete_request
from ..compat import NO_CONTENT, OK


def create_a_project(name, groups="", repo_url="", main_branch="", origin="", tags=None):
    """

    Args:
        name (str): The name that you would like to assign to the new Project. The Project name must be unique.
        groups (`list` of str): The group IDs of Groups (of users) that you would like to assign to this Project.
                     The ID of a Group can be found using the GET /auth/groups API.
                      A group must already exist in your account before a Project can be assigned to it.
                       Only users assigned to the designated Groups will have access to this Project.
        repo_url (str): The Git repo URL.
        main_branch (str): The Git branch of the source code that is designated as “primary” for this Project.
        origin (str): The manner by which the Project was created.
        tags (dict): The tags you want assigned to the Project.
                    Tags need to be formatted in key-value pairs.
                    example:
                    "tags": {"Tag01": "", "Severity": "high"}

    Returns:

    """

    relative_url = "/api/projects"
    if groups:
        if isinstance(groups, str):
            groups = [groups]
        elif isinstance(groups, list):
            groups = [str(item) for item in groups]

    data = {
        "name": name
    }
    if groups:
        data.update({"groups": groups})
    if repo_url:
        data.update({"repoUrl": repo_url})
    if main_branch:
        data.update({"mainBranch": main_branch})
    if origin:
        data.update({"origin": origin})
    if tags:
        data.update({"tags": tags})
    data = json.dumps(data)
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


def get_a_list_of_projects(offset=0, limit=20, ids=None, names=None, name=None, name_regex=None, groups=None,
                           tags_keys=None, tags_values=None, repo_url=None):
    """

    Args:
        offset (int): The number of results to skip before returning results
                    Default value : 0
        limit (int): The maximum number of results to return
                    Default value : 20
        ids (`list` of str): Filter results by project IDs.
                        Notes: Only exact matches are returned. OR operator is used for multiple IDs.
        names (`list` of str): Filter results for multiple project names.
                    Notes: Exact match, OR operator for multiple names, mutually exclusive to 'name' and 'name-regex'.
        name (str):  Filter results for a single project name.
                    Notes: Can be a substring of the name, mutually exclusive to 'names' and 'name-regex'.
        name_regex (str): Filter results by project name, by specifying a regex element of the name.
                            Note: Mutually exclusive to 'name' and 'names'.
        groups (`list` of str): Filter results by groups assigned to the project.
                                Notes: Only exact matches are returned. OR operator is used for multiple groups.
        tags_keys (`list` of str): Filter by tag keys (of the key:value pairs) associated with the projects.
                                    Note: OR operator is used for multiple keys.
        tags_values (`list` of str): Filter by tag values (of the key:value pairs) associated with the projects.
                                    Note: OR operator is used for multiple values.
        repo_url (str): Filter results by the project's repository url

    Returns:
        dict
        example:
        {
          "totalCount": 79,
          "filteredTotalCount": 79,
          "projects": [
            {
              "id": "a2feaa26-a515-4716-a2c5-b39c784980fb",
              "name": "JS_courselit",
              "createdAt": "2022-02-25T07:51:02.013774Z",
              "updatedAt": "2022-02-25T07:51:02.013774Z",
              "groups": [],
              "tags": {},
              "repoUrl": "",
              "mainBranch": ""
            },
          ]
        }
    """
    relative_url = "/api/projects"
    relative_url += "?offset={offset}&limit={limit}".format(
        offset=offset, limit=limit
    )
    if ids:
        for project_id in ids:
            relative_url += "&ids={project_id}".format(project_id=project_id)
    if names:
        for project_name in names:
            relative_url += "&names={project_name}".format(project_name=project_name)
    if name:
        relative_url += "&name={name}".format(name=name)
    if name_regex:
        relative_url += "&name-regex={name_regex}".format(name_regex=name_regex)
    if groups:
        for project_group in groups:
            relative_url += "&groups={project_group}".format(project_group=project_group)
    if tags_keys:
        for tags_key in tags_keys:
            relative_url += "&tags-keys={tags_key}".format(tags_key=tags_key)
    if tags_values:
        for tags_value in tags_values:
            relative_url += "&tags-values={tags_value}".format(tags_value=tags_value)
    if repo_url:
        relative_url += "&repo-url={repo_url}".format(repo_url=repo_url)

    response = get_request(relative_url=relative_url)
    response = response.json()
    projects = response.get("projects")
    if not projects:
        projects = []
    return {
        "totalCount": response.get("totalCount"),
        "filteredTotalCount": response.get("filteredTotalCount"),
        "projects": [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "groups": item.get("groups"),
                "repoUrl": item.get("repoUrl"),
                "mainBranch": item.get("mainBranch"),
                "origin": item.get("origin"),
                "createdAt": item.get("createdAt"),
                "updatedAt": item.get("updatedAt"),
                "tags": item.get("tags")
            } for item in projects
        ]
    }


def get_project_id_by_name(name):
    """

    Args:
        name (str):

    Returns:
        project_id (str)
    """
    pattern = "^" + name + "$"
    response = get_a_list_of_projects(name_regex=pattern)
    projects = response.get("projects")
    if not projects:
        return None
    return projects[0].get("id")


def delete_a_project(project_id):
    """

    Args:
        project_id (str):
    Returns:

    """
    is_successful = False

    if isinstance(project_id, str):
        relative_url = "/api/projects/{id}".format(id=project_id)
        response = delete_request(relative_url=relative_url)
        if response.status_code == NO_CONTENT:
            is_successful = True

    return is_successful
