from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import type_check, list_member_type_check
from .dto import (
    ProjectInput,
    Project, construct_project,
    ProjectsCollection, construct_projects_collection,
    RichProject, construct_rich_project,
    construct_subset_scan
)
from typing import List, Union

api_url = "/api/projects"


class ProjectsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_projects(self) -> List[Project]:
        projects = []
        offset = 0
        limit = 100
        page = 1
        project_collection = self.get_a_list_of_projects(offset=offset, limit=limit)
        total_count = int(project_collection.total_count)
        projects.extend(project_collection.projects)
        if total_count > limit:
            while True:
                offset = page * limit
                if offset >= total_count:
                    break
                project_collection = self.get_a_list_of_projects(offset=offset, limit=limit)
                page += 1
                projects.extend(project_collection.projects)
        return projects

    def create_a_project(self, project_input: ProjectInput) -> Project:
        """

        Args:
            project_input (ProjectInput):

        Returns:
            Project
        """
        relative_url = api_url
        response = self.api_client.post_request(relative_url=relative_url, json=project_input.to_dict())
        return construct_project(response.json())

    def get_a_list_of_projects(
            self, offset: int = 0, limit: int = 20, ids: List[str] = None, names: List[str] = None, name: str = None,
            name_regex: str = None, groups: List[str] = None, tags_keys: List[str] = None,
            tags_values: List[str] = None, repo_url: str = None
    ) -> ProjectsCollection:
        """

        Args:
            offset (int): The number of results to skip before returning results
                        Default value : 0
            limit (int): The maximum number of results to return
                        Default value : 20
            ids (`list` of str): Filter results by project IDs.
                            Notes: Only exact matches are returned. OR operator is used for multiple IDs.
            names (`list` of str): Filter results for multiple project names.
                        Notes: Exact match, OR operator for multiple names, mutually exclusive to 'name' and
                        'name-regex'.
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

        relative_url = api_url
        params = {
            "offset": offset, "limit": limit, "ids": ids, "names": names, "name": name, "name-regex": name_regex,
            "groups": groups, "tags-keys": tags_keys, "tags-values": tags_values, "repo-url": repo_url
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_projects_collection(response.json())

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
              "test": [
                ""
              ],
              "priority": [
                "high",
                "low"
              ]
            }
        """
        relative_url = api_url + "/tags"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json()

    def get_last_scan_info(
            self,
            offset: int = 0,
            limit: int = 20,
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
            sast_status (str): Sast engine status, please look at the scans API description for status options
            kics_status (str): Kics engine status, please look at the scans API description for status options
            sca_status (str): Sca engine status, please look at the scans API description for status options
            apisec_status (str): APISec engine status, please look at the scans API description for status options
            micro_engines_status (str): Micro Engines engine status, please look at the scans API description for status
                                options
            containers_status (str): Containers engine status, please look at the scans API description for status
                                    options
            use_main_branch (bool): A boolean flag to determine if the response should prioritize scans from
                                    the main branch. true:Return the last scan from the main branch if specified for the
                                     project, overriding the branch filter. false (default): Return the last scan
                                     regardless of the branch.
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
        relative_url = api_url + "/last-scan"
        params = {
            "offset": offset, "limit": limit,
            "project-ids": project_ids, "application-id": application_id, "scan-status": scan_status,
            "branch": branch, "engine": engine,
            "sast-status": sast_status, "kics-status": kics_status, "sca-status": sca_status,
            "apisec-status": apisec_status, "microengines-status": micro_engines_status,
            "containers-status": containers_status, "use-main-branch": use_main_branch,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        project_scan_map = response.json()
        return {
            project_id: construct_subset_scan(value) if value else None
            for project_id, value in project_scan_map.items()
        }

    def get_branches(
            self, offset: int = 0, limit: int = 20, project_id: str = None, branch_name: str = None
    ) -> List[str]:
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

        relative_url = api_url + "/branches"
        params = {
            "offset": offset, "limit": limit, "project-id": project_id, "branch-name": branch_name,
        }
        response = self.api_client.get_request(relative_url, params=params)
        return response.json()

    def get_a_project_by_id(self, project_id: str) -> RichProject:
        """

        Args:
            project_id (str):

        Returns:
            RichProject
        """
        relative_url = api_url + f"/{project_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        project = response.json()
        return construct_rich_project(project)

    def update_a_project(self, project_id: str, project_input: ProjectInput) -> bool:
        """
        Update Project. all parameters are covered by the input sent
        Args:
            project_id (str):
            project_input (ProjectInput):
        Returns:
            bool
        """
        if not project_id:
            return False
        relative_url = api_url + "/{id}".format(id=project_id)
        response = self.api_client.put_request(relative_url=relative_url, json=project_input.to_dict())
        return response.status_code == NO_CONTENT

    def delete_a_project(self, project_id: str) -> bool:
        """

        Args:
            project_id (str):
        Returns:
            bool
        """
        relative_url = api_url + f"/{project_id}"
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT

    def update_project_group(self, project_id: str, groups: List[str]) -> bool:
        """

       Args:
           project_id (str):
           groups (`list` of str):

       Returns:
           bool
       """
        relative_url = f"/api/projects/{project_id}"
        project = self.api_client.get_request(relative_url=relative_url)
        project_data = project.json()
        project_data['groups'] = groups
        response = self.api_client.put_request(relative_url=relative_url, json=project_data)
        return response.status_code == NO_CONTENT

    def update_primary_branch(self, project_id: str, branch_name: str) -> bool:
        """

        Args:
            project_id (str):
            branch_name (str): The desired branch name to be the primary branch
        Returns:
            bool
        """
        relative_url = f"/api/projects/{project_id}"
        project = self.api_client.get_request(relative_url=relative_url)
        project_data = project.json()
        project_data['mainBranch'] = branch_name
        response = self.api_client.put_request(relative_url=relative_url, json=project_data)
        return response.status_code == NO_CONTENT

    def add_project_single_tag(self, project_id: str, tag_key: str, tag_value: str) -> bool:
        """

        Args:
            project_id (str):
            tag_key (str):
            tag_value (str):
        Returns:
            bool
        """
        relative_url = f"/api/projects/{project_id}"
        project = self.api_client.get_request(relative_url=relative_url)
        project_data = project.json()
        if 'tags' not in project_data:
            project_data['tags'] = {}
        project_data['tags'][tag_key] = tag_value
        response = self.api_client.put_request(relative_url=relative_url, json=project_data)
        return response.status_code == NO_CONTENT

    def remove_project_single_tag(self, project_id: str, tag_key: str) -> bool:
        """

        Args:
            project_id (str):
            tag_key (str):
        Returns:
            bool
        """
        relative_url = f"/api/projects/{project_id}"
        project = self.api_client.get_request(relative_url=relative_url)
        project_data = project.json()
        if 'tags' in project_data:
            project_data['tags'].pop(tag_key)
        response = self.api_client.put_request(relative_url=relative_url, json=project_data)
        return response.status_code == NO_CONTENT

    def update_project_single_tag_key_value(self, project_id: str, tag_key: str, tag_value: str) -> bool:
        """

        Args:
            project_id (str):
            tag_key (str):
            tag_value (str):
        Returns:
            bool
        """
        relative_url = f"/api/projects/{project_id}"
        project = self.api_client.get_request(relative_url=relative_url)
        project_data = project.json()
        if 'tags' in project_data:
            project_data['tags'][tag_key] = tag_value
        # Update the project with the new tags
        response = self.api_client.put_request(relative_url=relative_url, json=project_data)
        return response.status_code == NO_CONTENT

    def get_projects_for_a_specific_application(self, app_id: str) -> ProjectsCollection:
        relative_url = f"/api/projects/app/{app_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_projects_collection(item)


def get_all_projects() -> List[Project]:
    return ProjectsAPI().get_all_projects()


def create_a_project(project_input: ProjectInput) -> Project:
    return ProjectsAPI().create_a_project(project_input=project_input)


def get_a_list_of_projects(
        offset: int = 0, limit: int = 20, ids: List[str] = None, names: List[str] = None, name: str = None,
        name_regex: str = None, groups: List[str] = None, tags_keys: List[str] = None, tags_values: List[str] = None,
        repo_url: str = None
) -> ProjectsCollection:
    return ProjectsAPI().get_a_list_of_projects(
        offset=offset, limit=limit, ids=ids, names=names, name=name, name_regex=name_regex, groups=groups,
        tags_keys=tags_keys, tags_values=tags_values, repo_url=repo_url
    )


def get_project_id_by_name(name) -> Union[str, None]:
    return ProjectsAPI().get_project_id_by_name(name=name)


def get_all_project_tags() -> dict:
    return ProjectsAPI().get_all_project_tags()


def get_last_scan_info(
        offset: int = 0, limit: int = 20, project_ids: List[str] = None, application_id: str = None,
        scan_status: str = None, branch: str = None, engine: str = None, sast_status: str = None,
        kics_status: str = None, sca_status: str = None, apisec_status: str = None, micro_engines_status: str = None,
        containers_status: str = None, use_main_branch: bool = False,
) -> dict:
    return ProjectsAPI().get_last_scan_info(
        offset=offset, limit=limit, project_ids=project_ids, application_id=application_id, scan_status=scan_status,
        branch=branch, engine=engine, sast_status=sast_status, kics_status=kics_status, sca_status=sca_status,
        apisec_status=apisec_status, micro_engines_status=micro_engines_status, containers_status=containers_status,
        use_main_branch=use_main_branch,
    )


def get_branches(
        offset: int = 0, limit: int = 20, project_id: str = None, branch_name: str = None
) -> List[str]:
    return ProjectsAPI().get_branches(offset=offset, limit=limit, project_id=project_id, branch_name=branch_name)


def get_a_project_by_id(project_id) -> RichProject:
    return ProjectsAPI().get_a_project_by_id(project_id=project_id)


def update_a_project(project_id: str, project_input: ProjectInput) -> bool:
    return ProjectsAPI().update_a_project(project_id=project_id, project_input=project_input)


def delete_a_project(project_id: str) -> bool:
    return ProjectsAPI().delete_a_project(project_id=project_id)


def update_project_group(project_id: str, groups: List[str]) -> bool:
    return ProjectsAPI().update_project_group(project_id=project_id, groups=groups)


def update_primary_branch(project_id: str, branch_name: str) -> bool:
    return ProjectsAPI().update_primary_branch(project_id=project_id, branch_name=branch_name)


def add_project_single_tag(project_id: str, tag_key: str, tag_value: str) -> bool:
    return ProjectsAPI().add_project_single_tag(project_id=project_id, tag_key=tag_key, tag_value=tag_value)


def remove_project_single_tag(project_id: str, tag_key: str) -> bool:
    return ProjectsAPI().remove_project_single_tag(project_id=project_id, tag_key=tag_key)


def update_project_single_tag_key_value(project_id: str, tag_key: str, tag_value: str) -> bool:
    return ProjectsAPI().update_project_single_tag_key_value(
        project_id=project_id, tag_key=tag_key, tag_value=tag_value
    )


def get_projects_for_a_specific_application(app_id: str) -> ProjectsCollection:
    return ProjectsAPI().get_projects_for_a_specific_application(app_id=app_id)
