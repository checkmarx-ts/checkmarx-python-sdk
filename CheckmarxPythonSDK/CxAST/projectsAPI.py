# encoding: utf-8
import json

from .httpRequests import get_request, post_request, put_request, delete_request
from ..compat import NO_CONTENT
from .utilities import get_url_param


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
        dict
        example: {
              "id": "string",
              "name": "string",
              "groups": [
                "string"
              ],
              "repoUrl": "string",
              "mainBranch": "string",
              "origin": "string",
              "createdAt": "2022-03-07T12:06:18.427Z",
              "updatedAt": "2022-03-07T12:06:18.427Z",
              "tags": {
                "test": "",
                "priority": "high"
              }
            }
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
    return response.json()


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
        example: {
          "totalCount": 0,
          "filteredTotalCount": 0,
          "projects": [
            {
              "id": "string",
              "name": "string",
              "groups": [
                "string"
              ],
              "repoUrl": "string",
              "mainBranch": "string",
              "origin": "string",
              "createdAt": "2022-03-02T03:36:17.102Z",
              "updatedAt": "2022-03-02T03:36:17.102Z",
              "tags": {
                "test": "",
                "priority": "high"
              }
            }
          ]
        }
    """
    relative_url = "/api/projects?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    relative_url += get_url_param("ids", ids)
    relative_url += get_url_param("names", names)
    relative_url += get_url_param("name", name)
    relative_url += get_url_param("name-regex", name_regex)
    relative_url += get_url_param("groups", groups)
    relative_url += get_url_param("tags-keys", tags_keys)
    relative_url += get_url_param("tags-values", tags_values)
    relative_url += get_url_param("repo-url", repo_url)

    # if ids and isinstance(ids, (list, tuple)):
    #     for project_id in ids:
    #         relative_url += "&ids={project_id}".format(project_id=project_id)
    # if names and isinstance(names, (list, tuple)):
    #     for project_name in names:
    #         relative_url += "&names={project_name}".format(project_name=project_name)
    # if name:
    #     relative_url += "&name={name}".format(name=name)
    # if name_regex:
    #     relative_url += "&name-regex={name_regex}".format(name_regex=name_regex)
    # if groups and isinstance(groups, (list, tuple)):
    #     for project_group in groups:
    #         relative_url += "&groups={project_group}".format(project_group=project_group)
    # if tags_keys and isinstance(tags_keys, (list, tuple)):
    #     for tags_key in tags_keys:
    #         relative_url += "&tags-keys={tags_key}".format(tags_key=tags_key)
    # if tags_values and isinstance(tags_values, (list, tuple)):
    #     for tags_value in tags_values:
    #         relative_url += "&tags-values={tags_value}".format(tags_value=tags_value)
    # if repo_url:
    #     relative_url += "&repo-url={repo_url}".format(repo_url=repo_url)

    response = get_request(relative_url=relative_url)
    return response.json()


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


def get_all_project_tags():
    """

    Returns:
        dict
        example: {
          "test": [
            ""
          ],
          "priority": [
            "high",
            "low"
          ]
        }
    """
    relative_url = "/api/projects/tags"
    response = get_request(relative_url=relative_url)
    return response.json()


def get_last_scan_info(offset=0, limit=20, project_ids=None, application_id=None, scan_status=None,
                       branch=None, engine=None):
    """
    Get a key-value map, key=[project id], value=[last scan (based on the filter)]

    Args:
        offset (int): The number of items to skip before starting to collect the result set
                        Default value : 0
        limit (int): The number of items to return
                        Default value : 20
        project_ids (`list` of str): Project ids, filtered by exact match. Mutually exclusive with application-id
        application_id (str): Application id, filtered by exact match. Mutually exclusive with project-ids.
        scan_status (str): Scan status, please look at the scans API description for status options
        branch (str): Git branch of the scan
        engine (str): Engine type of the scan

    Returns:
        dict
        example: {
          "project-id": {
            "id": "scan-id",
            "createdAt": "",
            "updatedAt": "",
            "status": "Completed",
            "userAgent": "user-agent",
            "initiator": "initiator",
            "branch": "branch",
            "engines": "[\"sast\", \"kics\"]",
            "sourceType": "github",
            "sourceOrigin": "Jenkins"
          }
        }
    """
    relative_url = "/api/projects/last-scan?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    if project_ids and isinstance(project_ids, (list, tuple)):
        for project_id in project_ids:
            relative_url += "&project-ids={project_id}".format(project_id=project_id)
    if application_id:
        relative_url += "&application-id={application_id}".format(application_id=application_id)
    if scan_status:
        relative_url += "&scan-status={scan_status}".format(scan_status=scan_status)
    if branch:
        relative_url += "&branch={branch}".format(branch=branch)
    if engine:
        relative_url += "&engine={engine}".format(engine=engine)
    response = get_request(relative_url=relative_url)
    return response.json()


def get_branches(offset=0, limit=20, project_id=None, branch_name=None):
    """
    Get a list of branches associated to this project sorted by date descended.
    Args:
        offset (int): The number of items to skip before starting to collect the result set
                        Default value : 0
        limit (int):  The number of items to return
                    Default value : 20
        project_id (str): Project id, filtered by exact match
        branch_name (str): Branch name. filtered by full or partial name

    Returns:
        list
        example: [
          "string"
        ]
    """
    relative_url = "/api/projects/branches?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    if project_id:
        relative_url += "&project-id={project_id}".format(project_id=project_id)
    if branch_name:
        relative_url += "&branch-name={branch_name}".format(branch_name=branch_name)
    response = get_request(relative_url)
    return response.json()


def get_a_project_by_id(project_id):
    """

    Args:
        project_id (str):

    Returns:
        dict
        example: {
          "id": "string",
          "name": "string",
          "applicationIds": [
            "string"
          ],
          "groups": [
            "string"
          ],
          "repoUrl": "string",
          "mainBranch": "string",
          "origin": "string",
          "createdAt": "2022-03-02T04:08:44.471Z",
          "updatedAt": "2022-03-02T04:08:44.471Z",
          "tags": {
            "test": "",
            "priority": "high"
          }
        }
    """
    relative_url = "/api/projects/{id}".format(id=project_id)
    response = get_request(relative_url=relative_url)
    return response.json()


def update_a_project(project_id, name=None, groups=None, repo_url=None, main_branch=None, origin=None, tags=None):
    """
    Update Project. all parameters are covered by the input sent

    Args:
        project_id (str):
        name (str): project name
        groups (`list` of str): The groups authorized for this project
        repo_url (str): The reprosentive repository URL
        main_branch (str): The Git main branch
        origin (str): The origin of project
        tags (dict):

    Returns:
        bool
    """
    is_successful = False
    if not project_id:
        return False
    relative_url = "/api/projects/{id}".format(id=project_id)

    data = {}
    if name:
        data.update({"name": name})
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
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == NO_CONTENT:
        is_successful = True

    return is_successful


def delete_a_project(project_id):
    """

    Args:
        project_id (str):
    Returns:
        bool
    """
    is_successful = False

    if isinstance(project_id, str):
        relative_url = "/api/projects/{id}".format(id=project_id)
        response = delete_request(relative_url=relative_url)
        if response.status_code == NO_CONTENT:
            is_successful = True

    return is_successful
