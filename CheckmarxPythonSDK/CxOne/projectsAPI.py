import logging
from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .dto import (
    ProjectInput,
    Project,
    ProjectsCollection,
    SubsetScan,
)
from typing import List, Union, Optional

logger = logging.getLogger(__name__)


class ProjectsAPI(object):

    def __init__(self, api_client: Optional[ApiClient] = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/projects"
        )

    def get_all_projects(self) -> List[Project]:
        """
        Get all projects

        Returns:
            List[Project]: List of all projects
        """
        logger.info("Start getting all projects")
        projects = []
        offset = 0
        limit = 500
        try:
            while True:
                project_collection = self.get_a_list_of_projects(
                    offset=offset,
                    limit=limit,
                )
                total_count = int(project_collection.total_count)
                projects.extend(project_collection.projects)
                if len(projects) >= total_count:
                    break
                offset += limit
                if offset > total_count:
                    break
        except Exception as e:
            logger.error(f"Error in get_all_projects: {str(e)}")
        return projects

    def create_a_project(self, project_input: ProjectInput) -> Project:
        """
        Args:
            project_input (ProjectInput):

        Returns:
            Project
        """
        response = self.api_client.call_api(
            method="POST", url=self.base_url,
            json={k: v for k, v in asdict(project_input).items() if v is not None}
        )
        return Project.from_dict(response.json())

    def get_a_list_of_projects(
        self,
        offset: int = 0,
        limit: int = 200,
        ids: List[str] = None,
        names: List[str] = None,
        name: str = None,
        name_regex: str = None,
        groups: List[str] = None,
        tags_keys: List[str] = None,
        tags_values: List[str] = None,
        repo_url: str = None,
    ) -> ProjectsCollection:
        """
        Args:
            offset (int): The number of results to skip before returning
                results. Default value: 0
            limit (int): The maximum number of results to return.
                Default value: 20
            ids (List[str]): Filter results by project IDs. Only exact
                matches are returned. OR operator for multiple IDs.
            names (List[str]): Filter results for multiple project names.
                Exact match, OR operator for multiple names. Mutually
                exclusive to 'name' and 'name-regex'.
            name (str): Filter results for a single project name. Can be
                a substring. Mutually exclusive to 'names' and
                'name-regex'.
            name_regex (str): Filter results by project name using a
                regex element. Mutually exclusive to 'name' and 'names'.
            groups (List[str]): Filter results by groups assigned to the
                project. Only exact matches. OR for multiple groups.
            tags_keys (List[str]): Filter by tag keys. OR for multiple
                keys.
            tags_values (List[str]): Filter by tag values. OR for
                multiple values.
            repo_url (str): Filter results by the project's repository
                url.

        Returns:
            ProjectsCollection
        """
        params = {
            "offset": offset,
            "limit": limit,
            "ids": ids,
            "names": names,
            "name": name,
            "name-regex": name_regex,
            "groups": groups,
            "tags-keys": tags_keys,
            "tags-values": tags_values,
            "repo-url": repo_url,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return ProjectsCollection.from_dict(response.json())

    def get_project_id_by_name(self, name: str) -> Union[str, None]:
        """
        Args:
            name (str):

        Returns:
            project_id (str)
        """
        pattern = "^" + name + "$"
        response = self.get_a_list_of_projects(name_regex=pattern)
        projects = response.projects
        if not projects:
            return None
        return projects[0].id

    def get_all_project_tags(self) -> dict:
        """
        Returns:
            dict
            example: {
              "test": [""],
              "priority": ["high", "low"]
            }
        """
        url = f"{self.base_url}/tags"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_last_scan_info(
        self,
        offset: int = 0,
        limit: int = 200,
        project_ids: List[str] = None,
        application_id: str = None,
        scan_status: str = None,
        branch: str = None,
        engine: str = None,
        sast_status: str = None,
        kics_status: str = None,
        sca_status: str = None,
        apisec_status: str = None,
        micro_engines_status: str = None,
        containers_status: str = None,
        use_main_branch: bool = False,
    ) -> dict:
        """
        Get a key-value map, key=[project id], value=[last scan].

        Args:
            offset (int): The number of items to skip before starting
                to collect the result set. Default: 0
            limit (int): The number of items to return. Default: 20
            project_ids (List[str]): Project ids, exact match. Mutually
                exclusive with application_id.
            application_id (str): Application id, exact match. Mutually
                exclusive with project_ids.
            scan_status (str): Scan status.
            branch (str): Git branch of the scan.
            engine (str): Engine type of the scan.
            sast_status (str): Sast engine status.
            kics_status (str): Kics engine status.
            sca_status (str): Sca engine status.
            apisec_status (str): APISec engine status.
            micro_engines_status (str): Micro Engines engine status.
            containers_status (str): Containers engine status.
            use_main_branch (bool): If true, return the last scan from
                the main branch if specified for the project.

        Returns:
            dict
        """
        url = f"{self.base_url}/last-scan"
        params = {
            "offset": offset,
            "limit": limit,
            "project-ids": project_ids,
            "application-id": application_id,
            "scan-status": scan_status,
            "branch": branch,
            "engine": engine,
            "sast-status": sast_status,
            "kics-status": kics_status,
            "sca-status": sca_status,
            "apisec-status": apisec_status,
            "microengines-status": micro_engines_status,
            "containers-status": containers_status,
            "use-main-branch": use_main_branch,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        project_scan_map = response.json()
        return {
            project_id: SubsetScan.from_dict(value) if value else None
            for project_id, value in project_scan_map.items()
        }

    def get_branches(
        self,
        offset: int = 0,
        limit: int = 200,
        project_id: str = None,
        branch_name: str = None,
    ) -> List[str]:
        """
        Get a list of branches associated to this project sorted by
        date descended.

        Args:
            offset (int): The number of items to skip before starting
                to collect the result set. Default: 0
            limit (int): The number of items to return. Default: 20
            project_id (str): Project id, filtered by exact match.
            branch_name (str): Branch name, filtered by full or partial
                name.

        Returns:
            list of str
        """
        url = f"{self.base_url}/branches"
        params = {
            "offset": offset,
            "limit": limit,
            "project-id": project_id,
            "branch-name": branch_name,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_a_project_by_id(self, project_id: str) -> Project:
        """
        Args:
            project_id (str):

        Returns:
            Project
        """
        url = f"{self.base_url}/{project_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return Project.from_dict(response.json())

    def update_a_project(
        self, project_id: str, project_input: ProjectInput
    ) -> bool:
        """
        Update Project. All parameters are covered by the input sent.

        Args:
            project_id (str):
            project_input (ProjectInput):

        Returns:
            bool
        """
        if not project_id:
            return False
        url = f"{self.base_url}/{project_id}"
        response = self.api_client.call_api(
            method="PUT", url=url,
            json={k: v for k, v in asdict(project_input).items() if v is not None}
        )
        return response.status_code == NO_CONTENT

    def update_specific_project_fields(
        self, project_id: str, project_input: ProjectInput
    ) -> bool:
        """
        Update specific project fields.

        Args:
            project_id (str):
            project_input (ProjectInput):

        Returns:
            bool
        """
        if not project_id:
            return False
        url = f"{self.base_url}/{project_id}"
        response = self.api_client.call_api(
            method="PATCH", url=url,
            json={k: v for k, v in asdict(project_input).items() if v is not None}
        )
        return response.status_code == NO_CONTENT

    def delete_a_project(self, project_id: str) -> bool:
        """
        Args:
            project_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/{project_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def update_project_group(
        self, project_id: str, groups: List[str]
    ) -> bool:
        """
        Args:
            project_id (str):
            groups (List[str]):

        Returns:
            bool
        """
        url = f"{self.base_url}/{project_id}"
        project = self.api_client.call_api(method="GET", url=url)
        project_data = project.json()
        project_data["groups"] = groups
        response = self.api_client.call_api(
            method="PUT", url=url, json=project_data
        )
        return response.status_code == NO_CONTENT

    def update_primary_branch(
        self, project_id: str, branch_name: str
    ) -> bool:
        """
        Args:
            project_id (str):
            branch_name (str): The desired branch name to be the primary
                branch.

        Returns:
            bool
        """
        url = f"{self.base_url}/{project_id}"
        project = self.api_client.call_api(method="GET", url=url)
        project_data = project.json()
        project_data["mainBranch"] = branch_name
        response = self.api_client.call_api(
            method="PUT", url=url, json=project_data
        )
        return response.status_code == NO_CONTENT

    def add_project_single_tag(
        self, project_id: str, tag_key: str, tag_value: str
    ) -> bool:
        """
        Args:
            project_id (str):
            tag_key (str):
            tag_value (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/{project_id}"
        project = self.api_client.call_api(method="GET", url=url)
        project_data = project.json()
        if "tags" not in project_data:
            project_data["tags"] = {}
        project_data["tags"][tag_key] = tag_value
        response = self.api_client.call_api(
            method="PUT", url=url, json=project_data
        )
        return response.status_code == NO_CONTENT

    def remove_project_single_tag(
        self, project_id: str, tag_key: str
    ) -> bool:
        """
        Args:
            project_id (str):
            tag_key (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/{project_id}"
        project = self.api_client.call_api(method="GET", url=url)
        project_data = project.json()
        if "tags" in project_data:
            project_data["tags"].pop(tag_key)
        response = self.api_client.call_api(
            method="PUT", url=url, json=project_data
        )
        return response.status_code == NO_CONTENT

    def update_project_single_tag_key_value(
        self, project_id: str, tag_key: str, tag_value: str
    ) -> bool:
        """
        Args:
            project_id (str):
            tag_key (str):
            tag_value (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/{project_id}"
        project = self.api_client.call_api(method="GET", url=url)
        project_data = project.json()
        if "tags" in project_data:
            project_data["tags"][tag_key] = tag_value
        response = self.api_client.call_api(
            method="PUT", url=url, json=project_data
        )
        return response.status_code == NO_CONTENT

    def get_projects_for_a_specific_application(
        self, app_id: str
    ) -> ProjectsCollection:
        url = f"{self.base_url}/app/{app_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return ProjectsCollection.from_dict(response.json())


def get_all_projects() -> List[Project]:
    return ProjectsAPI().get_all_projects()


def create_a_project(project_input: ProjectInput) -> Project:
    return ProjectsAPI().create_a_project(project_input=project_input)


def get_a_list_of_projects(
    offset: int = 0,
    limit: int = 200,
    ids: List[str] = None,
    names: List[str] = None,
    name: str = None,
    name_regex: str = None,
    groups: List[str] = None,
    tags_keys: List[str] = None,
    tags_values: List[str] = None,
    repo_url: str = None,
) -> ProjectsCollection:
    return ProjectsAPI().get_a_list_of_projects(
        offset=offset,
        limit=limit,
        ids=ids,
        names=names,
        name=name,
        name_regex=name_regex,
        groups=groups,
        tags_keys=tags_keys,
        tags_values=tags_values,
        repo_url=repo_url,
    )


def get_project_id_by_name(name: str) -> Union[str, None]:
    return ProjectsAPI().get_project_id_by_name(name=name)


def get_all_project_tags() -> dict:
    return ProjectsAPI().get_all_project_tags()


def get_last_scan_info(
    offset: int = 0,
    limit: int = 200,
    project_ids: List[str] = None,
    application_id: str = None,
    scan_status: str = None,
    branch: str = None,
    engine: str = None,
    sast_status: str = None,
    kics_status: str = None,
    sca_status: str = None,
    apisec_status: str = None,
    micro_engines_status: str = None,
    containers_status: str = None,
    use_main_branch: bool = False,
) -> dict:
    return ProjectsAPI().get_last_scan_info(
        offset=offset,
        limit=limit,
        project_ids=project_ids,
        application_id=application_id,
        scan_status=scan_status,
        branch=branch,
        engine=engine,
        sast_status=sast_status,
        kics_status=kics_status,
        sca_status=sca_status,
        apisec_status=apisec_status,
        micro_engines_status=micro_engines_status,
        containers_status=containers_status,
        use_main_branch=use_main_branch,
    )


def get_branches(
    offset: int = 0,
    limit: int = 200,
    project_id: str = None,
    branch_name: str = None,
) -> List[str]:
    return ProjectsAPI().get_branches(
        offset=offset,
        limit=limit,
        project_id=project_id,
        branch_name=branch_name,
    )


def get_a_project_by_id(project_id: str) -> Project:
    return ProjectsAPI().get_a_project_by_id(project_id=project_id)


def update_a_project(project_id: str, project_input: ProjectInput) -> bool:
    return ProjectsAPI().update_a_project(
        project_id=project_id, project_input=project_input
    )


def update_specific_project_fields(
    project_id: str, project_input: ProjectInput
) -> bool:
    return ProjectsAPI().update_specific_project_fields(
        project_id=project_id, project_input=project_input
    )


def delete_a_project(project_id: str) -> bool:
    return ProjectsAPI().delete_a_project(project_id=project_id)


def update_project_group(project_id: str, groups: List[str]) -> bool:
    return ProjectsAPI().update_project_group(
        project_id=project_id, groups=groups
    )


def update_primary_branch(project_id: str, branch_name: str) -> bool:
    return ProjectsAPI().update_primary_branch(
        project_id=project_id, branch_name=branch_name
    )


def add_project_single_tag(
    project_id: str, tag_key: str, tag_value: str
) -> bool:
    return ProjectsAPI().add_project_single_tag(
        project_id=project_id, tag_key=tag_key, tag_value=tag_value
    )


def remove_project_single_tag(project_id: str, tag_key: str) -> bool:
    return ProjectsAPI().remove_project_single_tag(
        project_id=project_id, tag_key=tag_key
    )


def update_project_single_tag_key_value(
    project_id: str, tag_key: str, tag_value: str
) -> bool:
    return ProjectsAPI().update_project_single_tag_key_value(
        project_id=project_id, tag_key=tag_key, tag_value=tag_value
    )


def get_projects_for_a_specific_application(
    app_id: str,
) -> ProjectsCollection:
    return ProjectsAPI().get_projects_for_a_specific_application(
        app_id=app_id
    )
