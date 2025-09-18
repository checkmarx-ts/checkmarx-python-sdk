from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from requests import Response
import json
from deprecated import deprecated
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import (type_check, list_member_type_check)

from .dto import (
    ScanInput,
    Scan, construct_scan,
    ScansCollection, construct_scans_collection,
    TaskInfo, construct_task_info,
)

api_url = "/api/scans"


class ScansAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_scan(self, scan_input: ScanInput) -> Scan:
        """
        Run a scan from a zip archive or Git repo
        Args:
            scan_input (ScanInput):

        Returns:
            Scan
        """
        type_check(scan_input, ScanInput)
        relative_url = api_url
        response = self.api_client.post_request(relative_url=relative_url, json=scan_input.to_dict())
        item = response.json()
        return construct_scan(item)

    @deprecated(version='0.5.3', reason='Use get_a_list_of_scans instead')
    def get_a_list_of_scan(self, *args, **kwargs):
        """
        """
        return self.get_a_list_of_scans(*args, **kwargs)

    def get_a_list_of_scans(
            self, offset: int = 0, limit: int = 20, scan_ids: List[str] = None, groups: List[str] = None,
            tags_keys: List[str] = None, tags_values: List[str] = None, statuses: List[str] = None,
            project_id: str = None, project_ids: List[str] = None, source_type: str = None,
            source_origin: str = None, from_date: str = None, sort: List[str] = ("+created_at", "+status"),
            field: List[str] = ("scan-ids",), search: str = None, to_date: str = None, project_names: List[str] = None,
            initiators: List[str] = None, branch: str = None, branches: List[str] = None
    ) -> ScansCollection:
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
                            (Exact match, case-sensitive, mutually exclusive to 'project-ids'.)
            project_ids (`list` of str): Filter results for scans of multiple projects, specified by project IDs.
                        (Exact match, case-sensitive, OR operator for multiple IDs, mutually exclusive to 'project-id'.)
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

        relative_url = api_url
        params = {
            "offset": offset, "limit": limit, "scan-ids": scan_ids, "groups": groups, "tags-keys": tags_keys,
            "tags-values": tags_values, "statuses": statuses, "project-id": project_id, "project-ids": project_ids,
            "source-type": source_type, "source-origin": source_origin, "from-date": from_date,
            "sort": ",".join(sort) if sort else None, "field": field, "search": search, "to-date": to_date,
            "project-names": project_names, "initiators": initiators, "branch": branch, "branches": branches,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        scans_collection = response.json()
        return construct_scans_collection(scans_collection)

    def get_all_scan_tags(self) -> dict:
        """
            Get all scan tags in your account
        """
        relative_url = api_url + "/tags"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json()

    def get_summary_of_the_status_of_the_scans(self) -> dict:
        """
        Get a summary of the status of the scans in your account.
        """
        relative_url = api_url + "/summary"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json()

    def get_the_list_of_available_config_as_code_template_files(self) -> dict:
        """
        Get the list of the available config-as-code template files that are under the dedicated directory.
        """
        relative_url = api_url + "/templates"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json()

    def get_the_config_as_code_template_file(self, file_name: str) -> str:
        """
        Get the config as code template file. example: '/templates/config.yml'
        """
        relative_url = api_url + "/templates/{file_name}".format(file_name=file_name)
        response = self.api_client.get_request(relative_url=relative_url)
        return response.text

    @deprecated(version='0.5.3', reason='Use get_a_scan_by_id instead')
    def get_scan_by_id(self, scan_id: str):
        return self.get_a_scan_by_id(scan_id)

    def get_a_scan_by_id(self, scan_id: str) -> Scan:
        """
        Get details about a specific scan, including the current status of the scan.
        Args:
            scan_id (str):

        Returns:
            Scan
        """
        relative_url = api_url + "/{id}".format(id=scan_id)
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_scan(item)

    def cancel_scan(self, scan_id: str) -> bool:
        """

        Args:
            scan_id (str):

        Returns:
            bool
        """
        relative_url = api_url + "/{id}".format(id=scan_id)
        response = self.api_client.patch_request(relative_url=relative_url, json={"status": "Canceled"})
        return response.status_code == NO_CONTENT

    def delete_scan(self, scan_id: str) -> bool:
        """

        Args:
            scan_id (str):

        Returns:
            bool
        """
        relative_url = api_url + "/{id}".format(id=scan_id)
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT

    def get_a_detailed_workflow_of_a_scan(self, scan_id: str) -> List[TaskInfo]:
        """

        Args:
            scan_id (str):

        Returns:
            List[TaskInfo]
        """
        relative_url = api_url + "/{id}/workflow".format(id=scan_id)
        response = self.api_client.get_request(relative_url=relative_url)
        items = response.json()
        return [
            construct_task_info(item) for item in items or []
        ]

    def sca_recalculate(self, project_id: str, branch: str) -> Response:
        """

        Args:
            project_id (str):
            branch (str):

        Returns:
            Response
        """
        relative_url = f"/api/scans/recalculate"

        scan_data = json.dumps({
            "project_id": f"{project_id}",
            "branch": f"{branch}",
            "engines": ["sca"],
            "config": [{"type": "sca", "value": {"enableContainersScan": True}}]
        })

        response = self.api_client.post_request(relative_url=relative_url, data=scan_data)
        return response

    def scan_by_repo_url(
            self, project_id: str, repo_url: str, branch: str, engines: List[str], tag: dict
    ) -> Response:
        """

        Args:
            project_id (str):
            repo_url (str):
            branch (str):
            engines (`list` of str): ["sast","sca", "kics", "apisec"]
            tag (json): {"test-all": ""}

        Returns:
            Response
        """
        relative_url = f"/api/scans"

        scan_data = {
            "type": "git",
            "handler": {
                "repoUrl": repo_url,
                "branch": branch,
                # "skipSubModules": False
            },
            "project": {
                "id": project_id,
                "tags": {}
            },
            "config": [],
            "tags": tag
        }

        engine_configs = {
            "sast": {"incremental": "false"},
            "sca": {},
            "kics": {},
            "apisec": {}
        }

        for engine in engines:
            if engine in engine_configs:
                scan_data["config"].append({
                    "type": engine,
                    "value": engine_configs[engine]
                })
            else:
                print(f"Warning: Engine '{engine}' is not supported and will be ignored.")

        response = self.api_client.post_request(relative_url=relative_url, data=json.dumps(scan_data))
        return response

    def get_scans_by_filters(
            self, offset: int = 0, limit: int = 20, scan_ids: List[str] = None, tags_keys: List[str] = None,
            tags_values: List[str] = None, statuses: List[str] = None, project_ids: List[str] = None,
            project_names: List[str] = None, branches: List[str] = None, initiators: List[str] = None,
            source_origins: List[str] = None, source_types: List[str] = None, search_id: str = None,
            sort_by: List[str] = ("+created_at", "+status")
    ) -> ScansCollection:
        """

        Args:
            offset (int):  The number of results to skip before returning results
            limit (int): The maximum number of results to return
            scan_ids (List of str): Filter results by scan IDs. Only exact matches are returned. (OR operator is used
                                    for multiple IDs.)
            tags_keys (List of str): Filter by tag keys (of the key:value pairs) associated with your scans. (OR
                                    operator is used for multiple keys.)
            tags_values (List of str): Filter by tag keys (of the key:value pairs) associated with your scans. (OR
                                        operator is used for multiple values.)
            statuses (List of str): Filter results by scans' execution status. (Case insensitive, OR operator for
                                    multiple statuses.)
            project_ids (List of str): Filter results for scans of multiple projects, specified by project IDs. (Exact
                match, case-sensitive, OR operator for multiple IDs, mutually exclusive to 'project-id'.)
            project_names (List of str): Filter scans by their project name
            branches (List of str): Filter results by the name of the Git branches.
            initiators (List of str): Filter scans by their initiator
            source_origins (List of str): Filter by scan origins.
            source_types (List of str): Source_type from scans table. return zip or github
            search_id (str): The scan searching with substring in all scan columns
            sort_by (List of str): Sort results by the specified parameter. Enter '-/+' for ascending/descending order,
            followed by the parameter.  [-created_at, +created_at, -status, +status, +branch, -branch, +initiator,
                -initiator, +user_agent, -user_agent, +name, -name]

        Returns:
            ScansCollection
        """
        relative_url = api_url + f"/byFilters"
        if isinstance(sort_by, tuple):
            sort_by = list(sort_by)
        sort_by = ",".join(sort_by) if sort_by else None
        data = {
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by
        }
        if scan_ids:
            data.update({"scan-ids": scan_ids})
        if tags_keys:
            data.update({"tags-keys": tags_keys})
        if tags_values:
            data.update({"tags-values": tags_values})
        if statuses:
            data.update({"statuses": statuses})
        if project_ids:
            data.update({"projectIDs": project_ids})
        if project_names:
            data.update({"project-names": project_names})
        if branches:
            data.update({"branches": branches})
        if initiators:
            data.update({"initiators": initiators})
        if source_origins:
            data.update({"source-origins": source_origins})
        if source_types:
            data.update({"source-types": source_types})
        if search_id:
            data.update({"searchID": search_id})
        response = self.api_client.post_request(relative_url=relative_url, data=json.dumps(data))
        scans_collection = response.json()
        return construct_scans_collection(scans_collection)


def create_scan(scan_input: ScanInput) -> Scan:
    return ScansAPI().create_scan(scan_input=scan_input)


@deprecated(version='0.5.3', reason='Use get_a_list_of_scans instead')
def get_a_list_of_scan(*args, **kwargs):
    return get_a_list_of_scans(*args, **kwargs)


def get_a_list_of_scans(
        offset: int = 0, limit: int = 20, scan_ids: List[str] = None, groups: List[str] = None,
        tags_keys: List[str] = None, tags_values: List[str] = None, statuses: List[str] = None,
        project_id: str = None, project_ids: List[str] = None, source_type: str = None,
        source_origin: str = None, from_date: str = None, sort: List[str] = ("+created_at", "+status"),
        field: List[str] = ("scan-ids",), search: str = None, to_date: str = None, project_names: List[str] = None,
        initiators: List[str] = None, branch: str = None, branches: List[str] = None
) -> ScansCollection:
    return ScansAPI().get_a_list_of_scans(
        offset=offset, limit=limit, scan_ids=scan_ids, groups=groups, tags_keys=tags_keys, tags_values=tags_values,
        statuses=statuses, project_id=project_id, project_ids=project_ids, source_type=source_type,
        source_origin=source_origin,
        from_date=from_date, sort=sort, field=field, search=search, to_date=to_date, project_names=project_names,
        initiators=initiators, branch=branch, branches=branches
    )


def get_all_scan_tags() -> dict:
    return ScansAPI().get_all_scan_tags()


def get_summary_of_the_status_of_the_scans() -> dict:
    return ScansAPI().get_summary_of_the_status_of_the_scans()


def get_the_list_of_available_config_as_code_template_files() -> dict:
    return ScansAPI().get_the_list_of_available_config_as_code_template_files()


def get_the_config_as_code_template_file(file_name: str) -> str:
    return ScansAPI().get_the_config_as_code_template_file(file_name=file_name)


@deprecated(version='0.5.3', reason='Use get_a_scan_by_id instead')
def get_scan_by_id(scan_id: str):
    return get_a_scan_by_id(scan_id=scan_id)


def get_a_scan_by_id(scan_id: str) -> Scan:
    return ScansAPI().get_a_scan_by_id(scan_id=scan_id)


def cancel_scan(scan_id: str) -> bool:
    return ScansAPI().cancel_scan(scan_id=scan_id)


def delete_scan(scan_id: str) -> bool:
    return ScansAPI().delete_scan(scan_id=scan_id)


def get_a_detailed_workflow_of_a_scan(scan_id: str) -> List[TaskInfo]:
    return ScansAPI().get_a_detailed_workflow_of_a_scan(scan_id=scan_id)


def sca_recalculate(project_id: str, branch: str) -> Response:
    return ScansAPI().sca_recalculate(project_id=project_id, branch=branch)


def scan_by_repo_url(
        project_id: str, repo_url: str, branch: str, engines: List[str], tag: dict = None
) -> Response:
    return ScansAPI().scan_by_repo_url(
        project_id=project_id, repo_url=repo_url, branch=branch, engines=engines, tag=tag
    )


def get_scans_by_filters(
        offset: int = 0, limit: int = 20, scan_ids: List[str] = None, tags_keys: List[str] = None,
        tags_values: List[str] = None, statuses: List[str] = None, project_ids: List[str] = None,
        project_names: List[str] = None, branches: List[str] = None, initiators: List[str] = None,
        source_origins: List[str] = None, source_types: List[str] = None, search_id: str = None,
        sort_by: List[str] = ("+created_at", "+status")
) -> ScansCollection:
    return ScansAPI().get_scans_by_filters(
        offset=offset, limit=limit, scan_ids=scan_ids, tags_keys=tags_keys, tags_values=tags_values,
        statuses=statuses, project_ids=project_ids, project_names=project_names, branches=branches,
        initiators=initiators, source_origins=source_origins, source_types=source_types, search_id=search_id,
        sort_by=sort_by,
    )
