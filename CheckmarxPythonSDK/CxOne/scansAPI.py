from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from httpx import Response
from deprecated import deprecated
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT

from .dto import (
    ScanInput,
    Scan,
    ScansCollection,
    TaskInfo,
)


class ScansAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/scans"
        )

    def create_scan(self, scan_input: ScanInput) -> Scan:
        """
        Run a scan from a zip archive or Git repo.

        Args:
            scan_input (ScanInput):

        Returns:
            Scan
        """
        response = self.api_client.call_api(
            method="POST", url=self.base_url, json={
                "type": scan_input.type,
                "handler": {
                    k: v for k, v in asdict(scan_input.handler).items()
                    if v is not None
                },
                "project": (
                    {
                        **({"id": scan_input.project.id} if scan_input.project.id else {}),
                        **({"tags": scan_input.project.tags} if scan_input.project.tags else {}),
                    }
                    if scan_input.project else scan_input.project
                ),
                "config": [
                    {k: v for k, v in asdict(c).items() if v is not None}
                    for c in (scan_input.configs or [])
                ],
                "tags": scan_input.tags,
            }
        )
        return Scan.from_dict(response.json())

    @deprecated(version="0.5.3", reason="Use get_a_list_of_scans instead")
    def get_a_list_of_scan(self, *args, **kwargs):
        """ """
        return self.get_a_list_of_scans(*args, **kwargs)

    def get_a_list_of_scans(
        self,
        offset: int = 0,
        limit: int = 20,
        scan_ids: List[str] = None,
        groups: List[str] = None,
        tags_keys: List[str] = None,
        tags_values: List[str] = None,
        statuses: List[str] = None,
        project_id: str = None,
        project_ids: List[str] = None,
        source_type: str = None,
        source_origin: str = None,
        from_date: str = None,
        sort: List[str] = ("+created_at", "+status"),
        field: List[str] = ("scan-ids",),
        search: str = None,
        to_date: str = None,
        project_names: List[str] = None,
        initiators: List[str] = None,
        branch: str = None,
        branches: List[str] = None,
    ) -> ScansCollection:
        """
        Get a list of scans with detailed information. Supports
        pagination and filters.

        Args:
            offset (int): Results to skip. Default: 0.
            limit (int): Max results to return. Default: 20.
            scan_ids (list of str): Filter by scan IDs (OR, exact).
            groups (list of str): Filter by project groups (OR, exact).
            tags_keys (list of str): Filter by tag keys (OR).
            tags_values (list of str): Filter by tag values (OR).
            statuses (list of str): Filter by execution status
                (case-insensitive, OR).
                Values: Queued, Running, Completed, Failed, Partial,
                Canceled
            project_id (str): Filter for a single project by ID
                (mutually exclusive with project_ids).
            project_ids (list of str): Filter for multiple projects by
                ID (OR, mutually exclusive with project_id).
            source_type (str): Filter by source type (zip or github).
            source_origin (str): Filter by source origin.
            from_date (str): Earliest scan date (RFC3339 format).
            sort (list of str): Sort fields, each "[-+]field".
                Values: created_at, status, branch, initiator,
                user_agent, name. Default: ["+created_at", "+status"]
            field (list of str): Filter field.
                Values: project-names, scan-ids, tags-keys, tags-values,
                branches, statuses, initiators, source-origins,
                source-types. Default: ["scan-ids"]
            search (str): Substring search across scan columns.
            to_date (str): Latest scan date (RFC3339 format).
            project_names (list of str): Filter by project name.
            initiators (list of str): Filter by scan initiator.
            branch (str): Filter by Git branch name (old naming).
            branches (list of str): Filter by Git branch names.

        Returns:
            ScansCollection
        """
        params = {
            "offset": offset,
            "limit": limit,
            "scan-ids": scan_ids,
            "groups": groups,
            "tags-keys": tags_keys,
            "tags-values": tags_values,
            "statuses": statuses,
            "project-id": project_id,
            "project-ids": project_ids,
            "source-type": source_type,
            "source-origin": source_origin,
            "from-date": from_date,
            "sort": ",".join(sort) if sort else None,
            "field": field,
            "search": search,
            "to-date": to_date,
            "project-names": project_names,
            "initiators": initiators,
            "branch": branch,
            "branches": branches,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return ScansCollection.from_dict(response.json())

    def get_all_scan_tags(self) -> dict:
        """Get all scan tags in your account."""
        url = f"{self.base_url}/tags"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_summary_of_the_status_of_the_scans(self) -> dict:
        """Get a summary of the status of the scans in your account."""
        url = f"{self.base_url}/summary"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_the_list_of_available_config_as_code_template_files(
        self,
    ) -> dict:
        """Get the list of available config-as-code template files."""
        url = f"{self.base_url}/templates"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_the_config_as_code_template_file(
        self, file_name: str
    ) -> str:
        """Get a config-as-code template file (e.g. '/templates/config.yml')."""
        url = f"{self.base_url}/templates/{file_name}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.text

    @deprecated(version="0.5.3", reason="Use get_a_scan_by_id instead")
    def get_scan_by_id(self, scan_id: str):
        return self.get_a_scan_by_id(scan_id)

    def get_a_scan_by_id(self, scan_id: str) -> Scan:
        """
        Get details about a specific scan.

        Args:
            scan_id (str):

        Returns:
            Scan
        """
        url = f"{self.base_url}/{scan_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return Scan.from_dict(response.json())

    def cancel_scan(self, scan_id: str) -> bool:
        """
        Args:
            scan_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/{scan_id}"
        response = self.api_client.call_api(
            method="PATCH", url=url, json={"status": "Canceled"}
        )
        return response.status_code == NO_CONTENT

    def delete_scan(self, scan_id: str) -> bool:
        """
        Args:
            scan_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/{scan_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def get_a_detailed_workflow_of_a_scan(
        self, scan_id: str
    ) -> List[TaskInfo]:
        """
        Args:
            scan_id (str):

        Returns:
            List[TaskInfo]
        """
        url = f"{self.base_url}/{scan_id}/workflow"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            TaskInfo.from_dict(item)
            for item in (response.json() or [])
        ]

    def sca_recalculate(self, project_id: str, branch: str) -> Response:
        """
        Args:
            project_id (str):
            branch (str):

        Returns:
            Response
        """
        url = f"{self.base_url}/recalculate"
        data = {
            "project_id": project_id,
            "branch": branch,
            "engines": ["sca"],
            "config": [
                {"type": "sca", "value": {"enableContainersScan": True}}
            ],
        }
        return self.api_client.call_api(
            method="POST", url=url, json=data
        )

    def scan_by_repo_url(
        self,
        project_id: str,
        repo_url: str,
        branch: str,
        engines: List[str],
        tag: dict,
    ) -> Response:
        """
        Args:
            project_id (str):
            repo_url (str):
            branch (str):
            engines (list of str): ["sast","sca", "kics", "apisec"]
            tag (dict): e.g. {"test-all": ""}

        Returns:
            Response
        """
        scan_data = {
            "type": "git",
            "handler": {"repoUrl": repo_url, "branch": branch},
            "project": {"id": project_id, "tags": {}},
            "config": [],
            "tags": tag,
        }
        engine_configs = {
            "sast": {"incremental": "false"},
            "sca": {},
            "kics": {},
            "apisec": {},
        }
        for engine in engines:
            if engine in engine_configs:
                scan_data["config"].append(
                    {"type": engine, "value": engine_configs[engine]}
                )
            else:
                print(
                    f"Warning: Engine '{engine}' is not supported "
                    f"and will be ignored."
                )
        return self.api_client.call_api(
            method="POST", url=self.base_url, json=scan_data
        )

    def get_scans_by_filters(
        self,
        offset: int = 0,
        limit: int = 20,
        scan_ids: List[str] = None,
        tags_keys: List[str] = None,
        tags_values: List[str] = None,
        statuses: List[str] = None,
        project_ids: List[str] = None,
        project_names: List[str] = None,
        branches: List[str] = None,
        initiators: List[str] = None,
        source_origins: List[str] = None,
        source_types: List[str] = None,
        search_id: str = None,
        sort_by: List[str] = ("+created_at", "+status"),
    ) -> ScansCollection:
        """
        Args:
            offset (int): Results to skip.
            limit (int): Max results to return.
            scan_ids (list of str): Filter by scan IDs (OR, exact).
            tags_keys (list of str): Filter by tag keys (OR).
            tags_values (list of str): Filter by tag values (OR).
            statuses (list of str): Filter by execution status (OR,
                case-insensitive).
            project_ids (list of str): Filter by project IDs (OR,
                exact, mutually exclusive with project_id).
            project_names (list of str): Filter by project name.
            branches (list of str): Filter by Git branch names.
            initiators (list of str): Filter by scan initiator.
            source_origins (list of str): Filter by scan origins.
            source_types (list of str): Filter by source type.
            search_id (str): Substring search across scan columns.
            sort_by (list of str): Sort fields, each "[-+]field".
                Values: created_at, status, branch, initiator,
                user_agent, name

        Returns:
            ScansCollection
        """
        url = f"{self.base_url}/byFilters"
        if isinstance(sort_by, tuple):
            sort_by = list(sort_by)
        sort_by_str = ",".join(sort_by) if sort_by else None
        data = {"offset": offset, "limit": limit, "sortBy": sort_by_str}
        if scan_ids:
            data["scan-ids"] = scan_ids
        if tags_keys:
            data["tags-keys"] = tags_keys
        if tags_values:
            data["tags-values"] = tags_values
        if statuses:
            data["statuses"] = statuses
        if project_ids:
            data["projectIDs"] = project_ids
        if project_names:
            data["project-names"] = project_names
        if branches:
            data["branches"] = branches
        if initiators:
            data["initiators"] = initiators
        if source_origins:
            data["source-origins"] = source_origins
        if source_types:
            data["source-types"] = source_types
        if search_id:
            data["searchID"] = search_id
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        return ScansCollection.from_dict(response.json())


def create_scan(scan_input: ScanInput) -> Scan:
    return ScansAPI().create_scan(scan_input=scan_input)


@deprecated(version="0.5.3", reason="Use get_a_list_of_scans instead")
def get_a_list_of_scan(*args, **kwargs):
    return get_a_list_of_scans(*args, **kwargs)


def get_a_list_of_scans(
    offset: int = 0,
    limit: int = 20,
    scan_ids: List[str] = None,
    groups: List[str] = None,
    tags_keys: List[str] = None,
    tags_values: List[str] = None,
    statuses: List[str] = None,
    project_id: str = None,
    project_ids: List[str] = None,
    source_type: str = None,
    source_origin: str = None,
    from_date: str = None,
    sort: List[str] = ("+created_at", "+status"),
    field: List[str] = ("scan-ids",),
    search: str = None,
    to_date: str = None,
    project_names: List[str] = None,
    initiators: List[str] = None,
    branch: str = None,
    branches: List[str] = None,
) -> ScansCollection:
    return ScansAPI().get_a_list_of_scans(
        offset=offset,
        limit=limit,
        scan_ids=scan_ids,
        groups=groups,
        tags_keys=tags_keys,
        tags_values=tags_values,
        statuses=statuses,
        project_id=project_id,
        project_ids=project_ids,
        source_type=source_type,
        source_origin=source_origin,
        from_date=from_date,
        sort=sort,
        field=field,
        search=search,
        to_date=to_date,
        project_names=project_names,
        initiators=initiators,
        branch=branch,
        branches=branches,
    )


def get_all_scan_tags() -> dict:
    return ScansAPI().get_all_scan_tags()


def get_summary_of_the_status_of_the_scans() -> dict:
    return ScansAPI().get_summary_of_the_status_of_the_scans()


def get_the_list_of_available_config_as_code_template_files() -> dict:
    return ScansAPI().get_the_list_of_available_config_as_code_template_files()


def get_the_config_as_code_template_file(file_name: str) -> str:
    return ScansAPI().get_the_config_as_code_template_file(
        file_name=file_name
    )


@deprecated(version="0.5.3", reason="Use get_a_scan_by_id instead")
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
    return ScansAPI().sca_recalculate(
        project_id=project_id, branch=branch
    )


def scan_by_repo_url(
    project_id: str,
    repo_url: str,
    branch: str,
    engines: List[str],
    tag: dict = None,
) -> Response:
    return ScansAPI().scan_by_repo_url(
        project_id=project_id,
        repo_url=repo_url,
        branch=branch,
        engines=engines,
        tag=tag,
    )


def get_scans_by_filters(
    offset: int = 0,
    limit: int = 20,
    scan_ids: List[str] = None,
    tags_keys: List[str] = None,
    tags_values: List[str] = None,
    statuses: List[str] = None,
    project_ids: List[str] = None,
    project_names: List[str] = None,
    branches: List[str] = None,
    initiators: List[str] = None,
    source_origins: List[str] = None,
    source_types: List[str] = None,
    search_id: str = None,
    sort_by: List[str] = ("+created_at", "+status"),
) -> ScansCollection:
    return ScansAPI().get_scans_by_filters(
        offset=offset,
        limit=limit,
        scan_ids=scan_ids,
        tags_keys=tags_keys,
        tags_values=tags_values,
        statuses=statuses,
        project_ids=project_ids,
        project_names=project_names,
        branches=branches,
        initiators=initiators,
        source_origins=source_origins,
        source_types=source_types,
        search_id=search_id,
        sort_by=sort_by,
    )
