# encoding: utf-8
from .httpRequests import get_request, post_request, put_request, delete_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    ProjectInput,
    Project,
    ProjectsCollection,
    RichProject,
    SubsetScan,
)


def __construct_project(project):
    return Project(
        project_id=project.get("id"),
        name=project.get("name"),
        groups=project.get("groups"),
        repo_url=project.get("repoUrl"),
        main_branch=project.get("mainBranch"),
        origin=project.get("origin"),
        created_at=project.get("createdAt"),
        updated_at=project.get("updatedAt"),
        tags=project.get("tags"),
        criticality=project.get("criticality"),
    )


def create_a_project(project_input):
    """

    Args:
        project_input (ProjectInput):

    Returns:
        Project
    """
    relative_url = "/api/projects"
    data = project_input.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return __construct_project(item)


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
        ProjectsCollection
    """
    type_check(offset, int)
    type_check(limit, int)
    type_check(ids, (list, tuple))
    type_check(names, (list, tuple))
    type_check(name, str)
    type_check(name_regex, str)
    type_check(groups, (list, tuple))
    type_check(tags_keys, (list, tuple))
    type_check(tags_values, (list, tuple))
    type_check(repo_url, str)

    list_member_type_check(ids, str)
    list_member_type_check(names, str)
    list_member_type_check(groups, str)
    list_member_type_check(tags_keys, str)
    list_member_type_check(tags_values, str)

    relative_url = "/api/projects?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    relative_url += get_url_param("ids", ids)
    relative_url += get_url_param("names", names)
    relative_url += get_url_param("name", name)
    relative_url += get_url_param("name-regex", name_regex)
    relative_url += get_url_param("groups", groups)
    relative_url += get_url_param("tags-keys", tags_keys)
    relative_url += get_url_param("tags-values", tags_values)
    relative_url += get_url_param("repo-url", repo_url)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return ProjectsCollection(
        total_count=item.get("totalCount"),
        filtered_total_count=item.get("filteredTotalCount"),
        projects=[
            __construct_project(project) for project in item.get("projects") or []
        ]
    )


def get_project_id_by_name(name):
    """

    Args:
        name (str):

    Returns:
        project_id (str)
    """
    pattern = "^" + name + "$"
    response = get_a_list_of_projects(name_regex=pattern)
    projects = response.projects
    if not projects:
        return None
    return projects[0].id


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
    """
    type_check(offset, int)
    type_check(limit, int)
    type_check(project_ids, (list, tuple))
    type_check(application_id, str)
    type_check(scan_status, str)
    type_check(branch, str)
    type_check(engine, str)

    list_member_type_check(project_ids, str)

    relative_url = "/api/projects/last-scan?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    relative_url += get_url_param("project-ids", project_ids)
    relative_url += get_url_param("application-id", application_id)
    relative_url += get_url_param("scan-status", scan_status)
    relative_url += get_url_param("branch", branch)
    relative_url += get_url_param("engine", engine)
    response = get_request(relative_url=relative_url)
    project_scan_map = response.json()
    return {
        key: SubsetScan(
            scan_id=value.get("id"),
            created_at=value.get("createdAt"),
            updated_at=value.get("updatedAt"),
            status=value.get("status"),
            user_agent=value.get("userAgent"),
            initiator=value.get("initiator"),
            branch=value.get("branch"),
            engines=value.get("engines"),
            source_type=value.get("sourceType"),
            source_origin=value.get("sourceOrigin")
        )
        for key, value in project_scan_map.items()
    }


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
        list of str
        example: [
          "string"
        ]
    """
    type_check(offset, int)
    type_check(limit, int)
    type_check(project_id, str)
    type_check(branch_name, str)

    relative_url = "/api/projects/branches?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    relative_url += get_url_param("project-id", project_id)
    relative_url += get_url_param("branch-name", branch_name)
    response = get_request(relative_url)
    return response.json()


def get_a_project_by_id(project_id):
    """

    Args:
        project_id (str):

    Returns:
        RichProject
    """
    relative_url = "/api/projects/{id}".format(id=project_id)
    response = get_request(relative_url=relative_url)
    project = response.json()
    return RichProject(
        project_id=project.get("id"),
        name=project.get("name"),
        application_ids=project.get("applicationIds"),
        groups=project.get("groups"),
        repo_url=project.get("repoUrl"),
        main_branch=project.get("mainBranch"),
        origin=project.get("origin"),
        created_at=project.get("createdAt"),
        updated_at=project.get("updatedAt"),
        tags=project.get("tags"),
        criticality=project.get("criticality"),
    )


def update_a_project(project_id, project_input):
    """
    Update Project. all parameters are covered by the input sent

    Args:
        project_id (str):
        project_input (ProjectInput):
    Returns:
        bool
    """
    is_successful = False
    if not project_id:
        return False
    relative_url = "/api/projects/{id}".format(id=project_id)
    data = project_input.get_post_data()
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
