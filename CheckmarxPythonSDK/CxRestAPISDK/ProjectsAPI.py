# encoding: utf-8
import os
import json
from .httpRequests import get_request, post_request, put_request, patch_request, delete_request, get_headers
from requests_toolbelt import MultipartEncoder
from CheckmarxPythonSDK.utilities.compat import OK, CREATED, ACCEPTED, NO_CONTENT
from CheckmarxPythonSDK.utilities.CxError import NotFoundError
from .TeamAPI import TeamAPI
from .sast.projects.dto import CxCreateProjectResponse, \
    CxIssueTrackingSystemDetail, CxIssueTrackingSystemField, \
    CxSharedRemoteSourceSettingsResponse, CxGitSettings, \
    CxIssueTrackingSystemType, CxIssueTrackingSystemFieldAllowedValue, \
    CxIssueTrackingSystem, CxLink, CxCustomRemoteSourceSettings, \
    CxProjectExcludeSettings, CxSVNSettings, CxURI, CxPerforceSettings, \
    CxTFSSettings, CxPreset
from .sast.projects.dto import construct_cx_project


class ProjectsAPI(object):
    """
    the projects API
    """
    @staticmethod
    def get_all_project_details(project_name=None, team_id=None, api_version="2.0"):
        """
        REST API: get all project details.
        For argument team_id, please consider using TeamAPI.get_team_id_by_full_name(team_full_name)

        Args:
            project_name (str, optional): Unique name of a specific project or projects
            team_id (int, str, optional): Unique Id of a specific team or teams.
                            default to id of the corresponding team full name in config.ini
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxProject`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects"
        optionals = []
        if project_name:
            optionals.append("projectName=" + str(project_name))
        if team_id:
            optionals.append("teamId=" + str(team_id))
        if optionals:
            relative_url += "?" + "&".join(optionals)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                construct_cx_project(item) for item in response.json()
            ]
        return result

    @staticmethod
    def create_project_with_default_configuration(project_name, team_id, is_public=True, api_version="1.0"):
        """
        REST API: create project

        Args:
            project_name (str):  Specifies the name of the project
            team_id (int, str): Specifies the id of the team that owns the project
                                default to the id of the team full name in config.ini
            is_public (boolean): Specifies whether the project is public or not
                                default True
            api_version (str, optional):

        Returns:
            :obj:`CxCreateProjectResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects"
        post_data = json.dumps(
            {
                "name": project_name,
                "owningTeam": team_id,
                "isPublic": is_public
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == CREATED:
            d = response.json()
            result = CxCreateProjectResponse(
                d.get("id"),
                CxLink(
                    rel=(d.get("link", {}) or {}).get("rel"),
                    uri=(d.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def get_project_id_by_project_name_and_team_full_name(project_name, team_full_name):
        """
        utility provided by SDK: get project id by project name, and team full name

        Args:
            project_name (str): project name under one team, different teams may have projects of the same name
            team_full_name (str): for example "/CxServer/SP/Company/Users"

        Returns:
            int: project id， if project not exists, return None
        """

        project_id = None

        team_id = TeamAPI().get_team_id_by_team_full_name(team_full_name=team_full_name)
        try:
            all_projects = ProjectsAPI.get_all_project_details(project_name=project_name, team_id=team_id)

            if all_projects and len(all_projects) == 1:
                project_id = all_projects[0].project_id
            return project_id
        except NotFoundError:
            return None

    @staticmethod
    def get_project_details_by_id(project_id, api_version="2.0"):
        """
        REST API: get project details by project id

        Args:
            project_id (int):  Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxProject`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        result = None
        relative_url = "/cxrestapi/projects/{id}".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = construct_cx_project(response.json())
        return result

    @staticmethod
    def update_project_by_id(project_id, project_name, team_id, custom_fields=(), api_version="1.0"):
        """
        update project info by project id

        Args:
            project_id (int): Unique Id of the project
            project_name (str, optional): Specifies the name of the project
            team_id (int, str, optional): Specifies the Id of the team that owns the project
            custom_fields (:obj:`list` of :obj:`CxCustomField`, optional):  specifies the custom field details
            api_version (str, optional):

        Returns:
            boolean: True means successful, False means not successful

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}".format(id=project_id)
        put_data = json.dumps(
            {
                "name": project_name,
                "owningTeam": team_id,
                "CustomFields": custom_fields
            }
        )
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        # In Python http module, HTTP status ACCEPTED is 202
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def update_project_name_team_id(project_id, project_name, team_id, api_version="1.0"):
        """
        REST API: update project name, team id

        Args:
            project_id (int):  consider using ProjectsAPI.get_project_id_by_name
            project_name (str, optional): Specifies the name of the project
            team_id (int, str): Specifies the Id of the team that owns the project
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}".format(id=project_id)
        patch_data = json.dumps(
            {
                "name": project_name,
                "owningTeam": team_id
            }
        )
        response = patch_request(relative_url=relative_url, data=patch_data, headers=get_headers(api_version))
        # In Python http module, HTTP status ACCEPTED is 202
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def delete_project_by_id(project_id, delete_running_scans=False, api_version="1.0"):
        """
        REST API: delete project by id

        Args:
            project_id (int):  Unique Id of the project
            delete_running_scans (boolean): Specifies whether running scans are to be deleted. Options are false/true.
                                Default=False, if not specified.
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}".format(id=project_id)
        delete_data = json.dumps({"deleteRunningScans": delete_running_scans})
        response = delete_request(relative_url=relative_url, data=delete_data, headers=get_headers(api_version))
        # In Python http module, HTTP status ACCEPTED is 202
        if response.status_code == ACCEPTED:
            result = True
        return result

    @staticmethod
    def create_project_if_not_exists_by_project_name_and_team_full_name(project_name, team_full_name):
        """
        create a project if it not exists by project name and a team full name

        Args:
            project_name (str):
            team_full_name (str):

        Returns:
            int: project id
        """
        team_id = TeamAPI().get_team_id_by_team_full_name(team_full_name)

        project_id = ProjectsAPI.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)

        if not project_id:
            project = ProjectsAPI.create_project_with_default_configuration(project_name, team_id, True)
            if project:
                project_id = project.id

        return project_id

    @staticmethod
    def delete_project_if_exists_by_project_name_and_team_full_name(project_name, team_full_name):
        """

        Args:
            project_name (str):
            team_full_name (str): for example "/CxServer/SP/Company/Users"

        Returns:
            boolean

        """
        result = False

        project_id = ProjectsAPI.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
        if project_id:
            result = ProjectsAPI.delete_project_by_id(project_id)
        return result

    @staticmethod
    def create_branched_project(project_id, branched_project_name, api_version="1.0"):
        """
        Create a branch of an existing project.

        Args:
            project_id (int): Unique Id of the project
            branched_project_name (str): specifies the name of the branched project
            api_version (str, optional):

        Returns:
            :obj:`CxCreateProjectResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/branch".format(id=project_id)
        post_data = json.dumps({"name": branched_project_name})
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxCreateProjectResponse(
                project_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def get_branch_project_status(branch_project_id, api_version="4.0"):
        result = False
        relative_url = "/cxrestapi/projects/branch/{}".format(branch_project_id)
        response = get_request(relative_url=relative_url,headers=get_headers(api_version=api_version))
        if response.status_code == OK:
            item = response.json()
            result = item['status']['id'] == 2
        return result

    @staticmethod
    def get_all_issue_tracking_systems(api_version="1.0"):
        """
        Get details of all issue tracking systems (e.g. Jira) currently registered to CxSAST.

        Args:
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxIssueTrackingSystem`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        result = None
        relative_url = "/cxrestapi/issueTrackingSystems"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxIssueTrackingSystem(
                    tracking_system_id=item.get("id"),
                    name=item.get("name"),
                    tracking_system_type=item.get("type"),
                    url=item.get("url")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_issue_tracking_system_id_by_name(name):
        """
        get issue tracking system id by name

        Args:
            name (str): issue tracking system name

        Returns:
            int: issue_tracking_system id
        """
        issue_tracking_systems = ProjectsAPI.get_all_issue_tracking_systems()
        a_dict = {item.name: item.id for item in issue_tracking_systems}
        return a_dict.get(name)

    @staticmethod
    def get_issue_tracking_system_details_by_id(issue_tracking_system_id, api_version="1.0"):
        """
        Get metadata for a specific issue tracking system (e.g. Jira) according to the Issue Tracking System Id.

        Args:
            issue_tracking_system_id (int):  Unique Id of the issue tracking system
            api_version (str, optional):

        Returns:
            dict

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/issueTrackingSystems/{id}/metadata".format(id=issue_tracking_system_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_list = response.json().get("projects")
            if a_list:
                a_dict = a_list[0]
                issue_types = a_dict.get("issueTypes")
                issue_type = issue_types[0] if issue_types else {}
                fields = issue_type.get("fields")
                field = fields[0] if fields else {}
                allowed_values = field.get("allowedValues", []) or []

                result = {
                    "projects": [
                        CxIssueTrackingSystemDetail(
                            tracking_system_detail_id=a_dict.get("id"),
                            name=a_dict.get("name"),
                            issue_types=[
                                CxIssueTrackingSystemType(
                                    issue_tracking_system_type_id=issue_type.get("id"),
                                    name=issue_type.get("name"),
                                    sub_task=issue_type.get("subtask"),
                                    fields=[
                                        CxIssueTrackingSystemField(
                                            tracking_system_field_id=field.get("id"),
                                            name=field.get("name"),
                                            multiple=field.get("multiple"),
                                            required=field.get("required"),
                                            supported=field.get("supported"),
                                            allowed_values=[
                                                CxIssueTrackingSystemFieldAllowedValue(
                                                    allowed_value_id=item.get("id"),
                                                    name=item.get("name")
                                                ) for item in allowed_values
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                }
        return result

    @staticmethod
    def get_project_exclude_settings_by_project_id(project_id, api_version="1.0"):
        """
        get details of a project's exclude folders/files settings according to the project Id.

        Args:
            project_id (int): Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxProjectExcludeSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/excludeSettings".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxProjectExcludeSettings(
                project_id=a_dict.get("projectId"),
                exclude_folders_pattern=a_dict.get("excludeFoldersPattern"),
                exclude_files_pattern=a_dict.get("excludeFilesPattern"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_project_exclude_settings_by_project_id(project_id, exclude_folders_pattern, exclude_files_pattern,
                                                   api_version="1.0"):
        """
        set a project's exclude folders/files settings according to the project Id.

        Args:
            project_id (int):  Unique Id of the project
            exclude_folders_pattern (str, optional): comma separated list of folders,
                        including wildcard patterns to exclude (e.g. add-ons, connectors, doc, CheckmarxPythonSDK, lib)
            exclude_files_pattern (str, optional): comma separated list of files,
                        including wildcard patterns to exclude (e.g. cvc3.js, spass.js, z3.js, readme.txt,
                        smt_solver.js, readme.txt, find_sql_injections.js, jquery.js, logic.js)
            api_version (str, optional):


        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/excludeSettings".format(id=project_id)
        put_data = json.dumps(
            {
                "excludeFoldersPattern": exclude_folders_pattern,
                "excludeFilesPattern": exclude_files_pattern
            }
        )
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        if response.status_code == OK:
            result = True
        return result

    @staticmethod
    def get_remote_source_settings_for_git_by_project_id(project_id, api_version="1.0"):
        """
        Get a specific project's remote source settings for a GIT repository according to the Project Id.

        Args:
            project_id (int): Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxGitSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/git".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxGitSettings(
                url=a_dict.get("url"),
                branch=a_dict.get("branch"),
                use_ssh=a_dict.get("useSsh"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_remote_source_setting_to_git(project_id, url, branch, private_key=None, api_version="1.0"):
        """
        Set a specific project's remote source location to a GIT repository using SSH protocol.

        Args:
            project_id (int): Unique Id of the project
            url (str): The url which is used to connect to the GIT repository (e.g. git@github.com:test/repo.git)
            branch (str): The branch of a GIT repository (e.g. refs/heads/master)
            private_key (str, optional): The private key (optional) which is used to connect to the GIT repository using
                                SSH protocol
                                (e.g. -----BEGIN RSA PRIVATE KEY-----
                                MIIJKgIBAAKCAgEahM6IR0lb4Rag4s5JM+xyEfKiUotGlHx
                                SkeRjzXyWwjX5dAfR3K7pzHzn0rSMN7yUYlhZDLKff6R
                                      -----END RSA PRIVATE KEY-----)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/git".format(id=project_id)
        post_data = json.dumps(
            {
                "url": url,
                "branch": branch,
                "privateKey": private_key
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_remote_source_settings_for_svn_by_project_id(project_id, api_version="1.0"):
        """
        get a specific project's remote source location settings for SVN repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxSVNSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/svn".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxSVNSettings(
                uri=CxURI(
                    absolute_url=(a_dict.get("uri", {}) or {}).get("absoluteUrl"),
                    port=(a_dict.get("uri", {}) or {}).get("port")
                ),
                paths=a_dict.get("paths", []),
                use_ssh=a_dict.get("useSsh", False),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_remote_source_settings_to_svn(project_id, absolute_url, port, paths, username, password,
                                          private_key=None, api_version="1.0"):
        """
        set a specific project's remote source location to a SVN repository using SSH protocol.

        Args:
            project_id (int):  Unique Id of the project
            absolute_url (str):  Specifies the absolute url (e.g. http://<server_ip>/svn/testrepo)
            port (int):  Specifies the port number of the uri (e.g. 8080)
            paths (:obj:`list` of :obj:`str`):  Specifies the list of paths to scan at SVN repository (e.g. /trunk )
            username (str):
            password (str):
            private_key (str, optional):  The private key (optional) which is used to connect to the SVN repository
                using SSH protocol
                (e.g. -----BEGIN RSA PRIVATE KEY-----
                MIIJKgIBAAKCAgEahM6IR0lb4Rag4s5JM+xyEfKiUotGlHx
                SkeRjzXyWwjX5dAfR3K7pzHzn0rSMN7yUYlhZDLKff6R
                     -----END RSA PRIVATE KEY-----)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/svn".format(id=project_id)
        post_data = json.dumps(
            {
                "uri": {
                    "absoluteUrl": absolute_url,
                    "port": port,
                },
                "paths": paths,
                "credentials": {
                    "userName": username,
                    "password": password,
                },
                "privateKey": private_key,
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_remote_source_settings_for_tfs_by_project_id(project_id, api_version="1.0"):
        """
        Get a specific project's remote source location settings for TFS repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxTFSSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/tfs".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxTFSSettings(
                uri=CxURI(
                    absolute_url=(a_dict.get("uri", {}) or {}).get("absoluteUrl"),
                    port=(a_dict.get("uri", {}) or {}).get("port"),
                ),
                paths=a_dict.get("paths"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_remote_source_settings_to_tfs(project_id, username, password, absolute_url, port, paths,
                                          api_version="1.0"):
        """
        Set a specific project's remote source location to a TFS repository.

        Args:
            project_id (int):  Unique Id of the project
            username (str):
            password (str):
            absolute_url (str):  Specifies the absolute url (e.g. http://<site_name>/tfs/DefaultCollection)
            port (int):  Specifies the port number of the uri (e.g. 8080)
            paths (:obj:`list` of :obj:`str`): Specifies the list of paths to scan at TFS repository
                                    (e.g. /Root/Optimization/V6.2.2.9-branch/CSharp/Graph, /Root/test)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/tfs".format(id=project_id)
        post_data = json.dumps(
            {
                "credentials": {
                    "userName": username,
                    "password": password
                },
                "uri": {
                    "absoluteUrl": absolute_url,
                    "port": port
                },
                "paths": paths,
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_remote_source_settings_for_custom_by_project_id(project_id, api_version="1.0"):
        """
        Get a specific project's remote source location settings for custom repository (e.g. source pulling)
         according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxCustomRemoteSourceSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/custom".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxCustomRemoteSourceSettings(
                path=a_dict.get("path"),
                pulling_command_id=a_dict.get("pullingCommandId"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_remote_source_setting_for_custom_by_project_id(project_id, path, pre_scan_command_id, username, password,
                                                           api_version="1.0"):
        """
        Set a specific project's remote source location settings for custom repository
        (e.g. source pulling) according to the Project Id.


        Args:
            project_id (int): Unique Id of the project
            path (str): Path to the network folders containing the project code
            pre_scan_command_id (int): Unique Id of script that pulls the source code
            username (str):
            password (str):
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/custom".format(id=project_id)
        post_data = json.dumps(
            {
                "path": path,
                "preScanCommandId": pre_scan_command_id,
                "credentials": {
                    "userName": username,
                    "password": password
                }
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_remote_source_settings_for_shared_by_project_id(project_id, api_version="1.0"):
        """
        Get a specific project's remote source location settings for shared repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxSharedRemoteSourceSettingsResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/shared".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxSharedRemoteSourceSettingsResponse(
                paths=a_dict.get("paths"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_remote_source_settings_to_shared(project_id, paths, username, password, api_version="1.0"):
        """
        Set a specific project's remote source location to a shared repository.

        Args:
            project_id (int):  Unique Id of the project
            paths (:obj:`list` of :obj:`str`):  Specifies the list of paths to scan at the shared repository
                            (e.g. \\\\storage\\qa\\projects_new\\CPP\\1_Under_70k\\cpp_22_LOC)
            username (str):
            password (sr):
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/shared".format(id=project_id)
        post_data = json.dumps(
            {
                "paths": paths,
                "credentials": {
                    "userName": username,
                    "password": password
                }
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_remote_source_settings_for_perforce_by_project_id(project_id, api_version="1.0"):
        """
        Get a specific project's remote source location settings for Perforce repository according to the Project Id.

        Args:
            project_id (int):  Unique Id of the specific project
            api_version (str, optional):

        Returns:
            :obj:`CxPerforceSettings`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/perforce".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxPerforceSettings(
                uri=CxURI(
                    absolute_url=(a_dict.get("uri", {}) or {}).get("absoluteUrl"),
                    port=(a_dict.get("uri", {}) or {}).get("port")
                ),
                paths=a_dict.get("paths"),
                browse_mode=a_dict.get("browseMode"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def set_remote_source_settings_to_perforce(project_id, username, password, absolute_url, port, paths,
                                               browse_mode, api_version="1.0"):
        """
        Set a specific project's remote source location to a Perforce repository.

        Args:
            project_id (int): Unique Id of the specific project
            username (str):
            password (str):
            absolute_url (str):  Specifies the absolute url (e.g. <server_ip>)
            port (int):  Specifies the port number of this Uri (e.g. 8080)
            paths (:obj:`list` of :obj:`str`): Specifies the list of paths to scan at Perforce repository
                                                (e.g. ////depot)
            browse_mode (str):  Specifies the browsing mode of the Perforce repository
                                (depot for shared or workspace for grouped).
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/perforce".format(id=project_id)
        post_data = json.dumps(
            {
                "credentials": {
                    "userName": username,
                    "password": password,
                },
                "uri": {
                    "absoluteUrl": absolute_url,
                    "port": port
                },
                "paths": paths,
                "browseMode": browse_mode
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def set_remote_source_setting_to_git_using_ssh(project_id, url, branch, private_key_file_path,
                                                   api_version="1.0"):
        """
        Set a specific project's remote source location to a GIT repository using the SSH protocol

        Args:
            project_id (int):  Unique Id of the project
            url (str):  The URL which is used to connect to the GIT repository (e.g. git@github.com:test_repo/test.git)
            branch (str): The branch of a GIT repository (e.g. refs/heads/master)
            private_key_file_path (str): The SSH certificate which is used to connect to the GIT repository
                                    using SSH protocol (multipart/form-data)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/git/ssh".format(id=project_id)
        file_name = os.path.basename(private_key_file_path)
        with open(private_key_file_path, "rb") as a_file:
            file_content = a_file.read()
        m = MultipartEncoder(
            fields={
                "url": url,
                "branch": branch,
                "privateKey": (file_name, file_content, "text/plain")
            }
        )
        headers = {"Content-Type": m.content_type}
        response = post_request(relative_url=relative_url, data=m, headers=get_headers(api_version, headers))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def set_remote_source_setting_to_svn_using_ssh(project_id, absolute_url, port, paths, private_key_file_path,
                                                   api_version="1.0"):
        """
        Set a specific project's remote source location to a SVN repository which uses the SSH protocol

        Args:
            project_id (int): Unique Id of the specific project
            absolute_url (str):  The URL which is used to connect to the SVN repository
                                (e.g. http://<server_ip>/svn/testrepo)
            port (int): Specifies the port number of SVN repository url
            paths (:obj:`list` of :obj:`str`): Specifies the paths of the SVN repository (e.g. /trunk)
            private_key_file_path (str): The SSH certificate which is used to connect to the SVN repository
                                         using SSH protocol (multipart/form-data)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        # TODO check, when have svn + ssh
        relative_url = "/cxrestapi/projects/{id}/sourceCode/remoteSettings/svn/ssh".format(id=project_id)
        file_name = os.path.basename(private_key_file_path)
        m = MultipartEncoder(
            fields={
                "absoluteUrl": absolute_url,
                "port": str(port),
                "paths": str(paths),
                "privateKey": (file_name, open(private_key_file_path, "rb"), "text/plain")
            }
        )
        headers = {"Content-Type": m.content_type}
        response = post_request(relative_url=relative_url, data=m, headers=get_headers(api_version, headers))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def upload_source_code_zip_file(project_id, zip_file_path, api_version="1.0"):
        """
        Upload a zip file that contains the source code for scanning.

        Args:
            project_id (int):  Unique Id of the project
            zip_file_path (str): absolute file path
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/sourceCode/attachments".format(id=project_id)
        file_name = os.path.basename(zip_file_path)
        m = MultipartEncoder(
            fields={
                "zippedSource": (file_name, open(zip_file_path, 'rb'), "application/zip")
            }
        )
        headers = {"Content-Type": m.content_type}
        response = post_request(relative_url=relative_url, data=m, headers=get_headers(api_version, headers))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def set_data_retention_settings_by_project_id(project_id, scans_to_keep=10, api_version="1.0"):
        """
        Set the data retention settings according to Project Id.

        Args:
            project_id (int):  Unique Id of the project
            scans_to_keep (int): The amount of scans to keep before they are deleted (1-1000 or null)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/projects/{id}/dataRetentionSettings".format(id=project_id)
        post_data = json.dumps(
            {
                "scansToKeep": scans_to_keep
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def set_issue_tracking_system_as_jira_by_id(project_id, issue_tracking_system_id, jira_project_id,
                                                issue_type_id, jira_fields, api_version="1.0"):
        """
        Set a specific issue tracking system as Jira according to Project Id.

        Args:
            project_id (int):  Unique Id of the project
            issue_tracking_system_id (int): Specifies the issue tracking system Id
            jira_project_id (str): Specifies the specific Id of Jira project
            issue_type_id (str): Specifies the Id of issue type
            jira_fields (:obj:`list` of :obj:`CxIssueTrackingSystemJiraField`) Specifies the list of fields associated
                                                        with the issue type
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        # TODO, check when have jira
        relative_url = "/cxrestapi/projects/{id}/issueTrackingSettings/jira".format(id=project_id)
        post_data = json.dumps(
            {
                "issueTrackingSystemId": issue_tracking_system_id,
                "jiraProjectId": jira_project_id,
                "issueType": {
                    "id": issue_type_id,
                    "fields": [
                        {
                            "id": field.id,
                            "values": field.values
                        } for field in jira_fields
                    ]
                }
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_all_preset_details(api_version="1.0"):
        """
        get details of all presets

        Args:
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxPreset`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        result = []
        relative_url = "/cxrestapi/sast/presets"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxPreset(
                    preset_id=item.get("id"),
                    name=item.get("name"),
                    owner_name=item.get("ownerName"),
                    link=CxLink(
                        rel=(item.get("link", {}) or {}).get("rel"),
                        uri=(item.get("link", {}) or {}).get("uri")
                    )
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_preset_id_by_name(preset_name):
        """

        Args:
            preset_name (str):

        Returns:
            int: preset id
        """
        all_presets = ProjectsAPI.get_all_preset_details()
        a_dict_preset_name_id = {item.name: item.id for item in all_presets}
        return a_dict_preset_name_id.get(preset_name)

    @staticmethod
    def get_preset_details_by_preset_id(preset_id, api_version="1.0"):
        """
        Get details of a specified preset by Id.

        Args:
            preset_id (int): Unique Id of the preset
            api_version (str, optional):

        Returns:
            :obj:`CxPreset`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/sast/presets/{id}".format(id=preset_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxPreset(
                preset_id=a_dict.get("id"),
                name=a_dict.get("name"),
                owner_name=a_dict.get("ownerName"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                ),
                query_ids=a_dict.get("queryIds")
            )
        return result

    @staticmethod
    def set_project_queue_setting(project_id, queue_keep_mode="KeepAll", scans_type="OnlyFull",
                                  include_scans_in_process=False, identical_code_only=False,
                                  api_version="2.1"):
        """

        Args:
            project_id (int):
            queue_keep_mode (str): Options: KeepAll, KeepNew, KeepOld.
            scans_type (str): Options: All, OnlyIncremental, OnlyFull
                        Note: • The automatic cancellation of parallel scans affects only public scans
                        and the selected scan type (Full / Incremental / All).
            include_scans_in_process (bool):
            identical_code_only (bool):
            api_version (str):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/sast/project/{id}/queueSettings".format(id=project_id)
        post_data = json.dumps(
            {
                "queueKeepMode": queue_keep_mode,
                "scansType": scans_type,
                "includeScansInProcess": include_scans_in_process,
                "identicalCodeOnly": identical_code_only
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def update_project_queue_setting(project_id, queue_keep_mode="KeepAll", scans_type="OnlyFull",
                                     include_scans_in_process=False, identical_code_only=False,
                                     api_version="2.1"):
        """

        Args:
            project_id (int):
            queue_keep_mode (str): Options: KeepAll, KeepNew, KeepOld.
            scans_type (str): Options: All, OnlyIncremental, OnlyFull
                        Note: • The automatic cancellation of parallel scans affects only public scans
                        and the selected scan type (Full / Incremental / All).
            include_scans_in_process (bool):
            identical_code_only (bool):
            api_version (str):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/sast/project/{id}/queueSettings".format(id=project_id)
        put_data = json.dumps(
            {
                "queueKeepMode": queue_keep_mode,
                "scansType": scans_type,
                "includeScansInProcess": include_scans_in_process,
                "identicalCodeOnly": identical_code_only
            }
        )
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result
