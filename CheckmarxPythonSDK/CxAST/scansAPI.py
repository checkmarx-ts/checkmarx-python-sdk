# encoding: utf-8
import json

from deprecated import deprecated
from .httpRequests import get_request, post_request, delete_request, patch_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import (get_url_param, type_check, list_member_type_check)

from .dto import (
    ScanInput,
    Scan,
    StatusDetails,
    ScansCollection,
    TaskInfo,
)


def __construct_scan(item):
    return Scan(
        scan_id=item.get("id"),
        status=item.get("status"),
        status_details=[
            StatusDetails(
                name=detail.get("name"),
                status=detail.get("status"),
                details=detail.get("details"),
            )
            for detail in item.get("statusDetails") or []
        ],
        position_in_queue=item.get("positionInQueue"),
        project_id=item.get("projectId"),
        branch=item.get("branch"),
        commit_id=item.get("commitId"),
        commit_tag=item.get("commitTag"),
        upload_url=item.get("uploadUrl"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        user_agent=item.get("userAgent"),
        initiator=item.get("initiator"),
        tags=item.get("tags"),
        metadata=item.get("metadata"),
    )


def create_scan(scan_input):
    """
    Run a scan from a zip archive or Git repo
    Args:
        scan_input (ScanInput):

    Returns:
        Scan
    """
    type_check(scan_input, ScanInput)
    relative_url = "/api/scans"
    data = scan_input.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return __construct_scan(item)


@deprecated(version='0.5.3', reason='Use get_a_list_of_scans instead')
def get_a_list_of_scan(*args, **kwargs):
    """
    """
    return get_a_list_of_scans(*args, **kwargs)


def get_a_list_of_scans(offset=0, limit=20, scan_ids=None, groups=None, tags_keys=None, tags_values=None,
                        statuses=None, project_id=None, project_ids=None, source_type=None, source_origin=None,
                        from_date=None, sort=None, field=None, search=None, to_date=None, project_names=None,
                        initiators=None, branch=None, branches=None):
    """
    Get a list of scans, with detailed information about each scan. You can limit the results by using pagination
    and/or setting filters.

    Args:
        offset (int): The number of results to skip before returning results
                    Default value : 0
        limit (int): The max. number of results to return
                    Default value : 20
        scan_ids (`list` of str): Filter results by scan IDs. Only exact matches are returned.
                        (OR operator is used for multiple IDs.)
        groups (`list` of str): Filter results by groups assigned to the project. Only exact matches are returned.
                    (OR operator is used for multiple groups.)
        tags_keys (`list` of str): Filter by tag keys (of the key:value pairs) associated with your scans.
                    (OR operator is used for multiple keys.)
        tags_values (`list` of str): Filter by tag keys (of the key:value pairs) associated with your scans.
                            (OR operator is used for multiple values.)
        statuses (`list` of str): Filter results by scans' execution status.
                    (Case insensitive, OR operator for multiple statuses.)
                    Available values : Queued, Running, Completed, Failed, Partial, Canceled
        project_id (str): Filter results for scans of a single project, specified by project ID.
                        (Exact match, case sensitive, mutually exclusive to 'project-ids'.)
        project_ids (`list` of str): Filter results for scans of multiple projects, specified by project IDs.
                    (Exact match, case sensitive, OR operator for multiple IDs, mutually exclusive to 'project-id'.)
        source_type (str): source_type from scans table. return zip or github
        source_origin (str): source_origin from scans table. return webapp or jenkins or etc.
        from_date (str): Filter for the earliest date and time of a scan for which you would like to show results.
                    Time must be entered in RFC3339 Date (Extend) format (e.g. 2021-06-02T12:14:18.028555Z)
        sort (`list` of str): Sort results by the specified parameter.
                            Enter '+/-' for ascending/descending order, followed by the parameter.
                Available values : -created_at, +created_at, -status, +status, +branch, -branch,
                 +initiator, -initiator, +user_agent, -user_agent, +name, -name
                Default value : List [ "+created_at", "+status" ]
        field (`list` of str): The filter
                Available values : project-names, scan-ids, tags-keys, tags-values, branches,
                statuses, initiators, source-origins, source-types
                Default value : List [ "scan-ids" ]
        search (str): The scan searching with substring in all scan columns
        to_date (str): Filter for the latest date and time of a scan for which you would like to show results.
                Time must be entered in RFC3339 Date (Extend) format (e.g. 2021-06-02T12:14:18.028555Z)
        project_names (`list` of str): Filter scans by their project name
        initiators (`list` of str): Filter scans by their initiator
        branch (str): Filter results by the name of the Git branch. Old naming.
        branches (`list` of str): Filter results by the name of the Git branches

    Returns:
        ScansCollection
    """
    type_check(offset, int)
    type_check(limit, int)
    type_check(scan_ids, (list, tuple))
    type_check(groups, (list, tuple))
    type_check(tags_keys, (list, tuple))
    type_check(tags_values, (list, tuple))
    type_check(statuses, (list, tuple))
    type_check(project_id, str)
    type_check(project_ids, (list, tuple))
    type_check(source_type, str)
    type_check(source_origin, str)
    type_check(from_date, str)
    type_check(sort, (list, tuple))
    type_check(field, (list, tuple))
    type_check(search, str)
    type_check(to_date, str)
    type_check(project_names, (list, tuple))
    type_check(initiators, (list, tuple))
    type_check(branch, str)
    type_check(branches, (list, tuple))

    list_member_type_check(scan_ids, str)
    list_member_type_check(groups, str)
    list_member_type_check(tags_keys, str)
    list_member_type_check(tags_values, str)
    list_member_type_check(project_ids, str)
    list_member_type_check(sort, str)
    list_member_type_check(field, str)
    list_member_type_check(project_names, str)
    list_member_type_check(initiators, str)
    list_member_type_check(branches, str)

    relative_url = "/api/scans?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    relative_url += get_url_param("scan-ids", scan_ids)
    relative_url += get_url_param("groups", groups)
    relative_url += get_url_param("tags-keys", tags_keys)
    relative_url += get_url_param("tags-values", tags_values)
    relative_url += get_url_param("statuses", statuses)
    relative_url += get_url_param("project-id", project_id)
    relative_url += get_url_param("project-ids", project_ids)
    relative_url += get_url_param("source-type", source_type)
    relative_url += get_url_param("source-origin", source_origin)
    relative_url += get_url_param("from-date", from_date)
    relative_url += get_url_param("sort", sort)
    relative_url += get_url_param("field", field)
    relative_url += get_url_param("search", search)
    relative_url += get_url_param("to-date", to_date)
    relative_url += get_url_param("project-names", project_names)
    relative_url += get_url_param("initiators", initiators)
    relative_url += get_url_param("branch", branch)
    relative_url += get_url_param("branches", branches)

    response = get_request(relative_url=relative_url)
    scans_collection = response.json()
    return ScansCollection(
        total_count=scans_collection.get("totalCount"),
        filtered_total_count=scans_collection.get("filteredTotalCount"),
        scans=[__construct_scan(item) for item in scans_collection.get("scans") or []]
    )


def get_all_scan_tags():
    """
        Get all scan tags in your account
    Returns:
        dict
    """
    relative_url = "/api/scans/tags"
    response = get_request(relative_url=relative_url)
    return response.json()


def get_summary_of_the_status_of_the_scans():
    """
    Get a summary of the status of the scans in your account.
    Returns:
        dict
    """
    relative_url = "/api/scans/summary"
    response = get_request(relative_url=relative_url)
    return response.json()


def get_the_list_of_available_config_as_code_template_files():
    """
    Get the list of the available config-as-code template files that are under the dedicated directory.
    Returns:
        dict
    """
    relative_url = "/api/scans/templates"
    response = get_request(relative_url=relative_url)
    return response.json()


def get_the_config_as_code_template_file(file_name):
    """
    Get the config as code template file. example: '/templates/config.yml'
    Args:
        file_name (str):
    Returns:
        str
    """
    relative_url = "/api/scans/templates/{file_name}".format(file_name=file_name)
    response = get_request(relative_url=relative_url)
    return response.text


@deprecated(version='0.5.3', reason='Use get_a_scan_by_id instead')
def get_scan_by_id(scan_id):
    return get_a_scan_by_id(scan_id)


def get_a_scan_by_id(scan_id):
    """
    Get details about a specific scan, including the current status of the scan.
    Args:
        scan_id (str):

    Returns:
        Scan
    """
    relative_url = "/api/scans/{id}".format(id=scan_id)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return __construct_scan(item)


def cancel_scan(scan_id):
    """

    Args:
        scan_id (str):

    Returns:
        str  example:  "Canceled"
    """
    is_successful = False
    relative_url = "/api/scans/{id}".format(id=scan_id)
    data = json.dumps({"status": "Canceled"})
    response = patch_request(relative_url=relative_url, data=data)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def delete_scan(scan_id):
    """

    Args:
        scan_id (str):

    Returns:

    """
    is_successful = False
    relative_url = "/api/scans/{id}".format(id=scan_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def get_a_detailed_workflow_of_a_scan(scan_id):
    """

    Args:
        scan_id (str):

    Returns:
        list of TaskInfo
    """
    relative_url = "/api/scans/{id}/workflow".format(id=scan_id)
    response = get_request(relative_url=relative_url)
    items = response.json()
    return [
        TaskInfo(
            source=item.get("Source"),
            timestamp=item.get("Timestamp"),
            info=item.get("Info"),
        ) for item in items or []
    ]
