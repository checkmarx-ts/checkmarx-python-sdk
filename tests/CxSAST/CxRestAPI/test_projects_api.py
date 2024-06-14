"""
    tests.test_projects_api

    :copyright Checkmarx
    :license GPL-3

"""
import time
from os.path import normpath, join, dirname

from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI
from CheckmarxPythonSDK.utilities.CxError import CxError
team_full_name = "/CxServer"


def test_get_all_project_details():
    projects_api = ProjectsAPI()
    all_projects = projects_api.get_all_project_details(api_version="2.1")
    assert all_projects is not None
    if len(all_projects) > 0:
        first_project = all_projects[0]
        project_detail = projects_api.get_all_project_details(first_project.name, first_project.team_id,
                                                              api_version="2.1")
        assert project_detail is not None


def test_create_project_with_default_configuration():
    projects_api = ProjectsAPI()

    project_name = "test1"
    projects_api.delete_project_if_exists_by_project_name_and_team_full_name(project_name, team_full_name)

    team_api = TeamAPI()
    team_id = team_api.get_team_id_by_team_full_name(team_full_name)
    response = projects_api.create_project_with_default_configuration(project_name, team_id, True)
    assert response.id is not None


def test_get_project_id_by_name():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    assert project_id is not None


def test_get_project_details_by_id():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    if project_id:
        project = projects_api.get_project_details_by_id(project_id)
        assert project.project_id is not None


def test_update_project_by_id():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)

    branched_project_name = "test_update"
    projects_api.delete_project_if_exists_by_project_name_and_team_full_name(branched_project_name, team_full_name)
    team_id = TeamAPI().get_team_id_by_team_full_name(team_full_name)
    if project_id:
        result = projects_api.update_project_by_id(project_id, project_name=branched_project_name, team_id=team_id)
        assert result is True


def test_update_project_name_team_id():
    projects_api = ProjectsAPI()
    team_id = TeamAPI().get_team_id_by_team_full_name(team_full_name)
    project_name = "test_update"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    if project_id:
        result = projects_api.update_project_name_team_id(project_id, project_name="test1", team_id=team_id)
        assert result is True


def test_delete_project_by_id():
    projects_api = ProjectsAPI()
    project_name = "test1"
    result = projects_api.delete_project_if_exists_by_project_name_and_team_full_name(project_name, team_full_name)
    assert result is True


def test_create_branched_project():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(
        project_name, team_full_name
    )

    branched_project_name = "test-branch"
    projects_api.delete_project_if_exists_by_project_name_and_team_full_name(branched_project_name, team_full_name)
    if project_id:
        branched_project = projects_api.create_branched_project(project_id, branched_project_name)
        assert branched_project is not None


def test_get_branch_project_status():
    projects_api = ProjectsAPI()
    branch_project_id = projects_api.get_project_id_by_project_name_and_team_full_name("test-branch", "/CxServer")
    time.sleep(120)
    result = projects_api.get_branch_project_status(branch_project_id)
    assert result is True
    projects_api.delete_project_by_id(branch_project_id)


def test_get_all_issue_tracking_systems():
    # projects_api = ProjectsAPI()
    # issue_tracking_systems = projects_api.get_all_issue_tracking_systems()
    # assert issue_tracking_systems is not None
    pass


def test_get_issue_tracking_system_id_by_name():
    # projects_api = ProjectsAPI()
    # issue_tracking_system_name = "globe-demo"
    # issue_tracking_system_id = projects_api.get_issue_tracking_system_id_by_name(issue_tracking_system_name)
    # assert issue_tracking_system_id is not None
    pass


def test_get_issue_tracking_system_details_by_id():
    projects_api = ProjectsAPI()
    issue_tracking_systems = projects_api.get_all_issue_tracking_systems()
    if issue_tracking_systems and len(issue_tracking_systems) > 0:
        issue_tracking_system_id = issue_tracking_systems[0].id
        try:
            issue_tracking_system = projects_api.get_issue_tracking_system_details_by_id(issue_tracking_system_id)
            assert issue_tracking_system is not None
        except CxError:
            pass


def test_set_project_exclude_settings_by_project_id():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    exclude_folders_pattern = "docs,tests,example"
    exclude_files_pattern = "*.txt,*.doc, *.csv"
    result = projects_api.set_project_exclude_settings_by_project_id(project_id, exclude_folders_pattern,
                                                                     exclude_files_pattern)
    assert result is True


def test_get_project_exclude_settings_by_project_id():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    exclude_settings = projects_api.get_project_exclude_settings_by_project_id(project_id)
    assert exclude_settings is not None


def test_set_remote_source_setting_to_git():
    projects_api = ProjectsAPI()
    project_name = "test1"
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
                                                                                              team_full_name)
    url = "https://github.com/HappyY19/Cx-REST-API-SDK-Python.git"
    branch = "refs/heads/master"
    result = projects_api.set_remote_source_setting_to_git(project_id, url, branch, authentication="none")
    assert result is True

    url = "https://github.com/HappyY19/CxSoccer.git"
    branch = "refs/heads/master"
    username = "***"
    password = "***!"
    result = projects_api.set_remote_source_setting_to_git(project_id, url, branch,
                                                        authentication="credentials",
                                                           username=username,
                                                           password=password)
    assert result is True

    github_personal_access_token = "***"
    result = projects_api.set_remote_source_setting_to_git(project_id, url, branch, authentication="PAT", pat=github_personal_access_token)
    assert result is True

    private_key_file_path = r"C:\Users\HappyY\.ssh\id_rsa"
    with open(private_key_file_path, 'r') as f:
        private_key_content = f.read()
        try:
            result = projects_api.set_remote_source_setting_to_git(project_id, url, branch, authentication="ssh",
                                                                   private_key=private_key_content)
            assert result is True
        except CxError:
            pass


def test_get_remote_source_settings_for_git_by_project_id():
    projects_api = ProjectsAPI()
    project_name = "jvl_git"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    git_settings = projects_api.get_remote_source_settings_for_git_by_project_id(project_id)
    assert git_settings is not None


def test_set_remote_source_settings_to_svn():
    """
    projects_api = ProjectsAPI()
    project_name = "happy-svn"
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
                                                                                              team_full_name)

    absolute_url = "svn://123.207.221.18/spring-mybatis-dva/happy"
    port = 3690
    paths = ['/src']
    username = "happy"
    result = projects_api.set_remote_source_settings_to_svn(project_id, absolute_url, port, paths, username, "")
    assert result is True
    """


def test_get_remote_source_settings_for_svn_by_project_id():
    """
    projects_api = ProjectsAPI()
    project_name = "happy-svn"
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    svn_settings = projects_api.get_remote_source_settings_for_svn_by_project_id(project_id)
    assert svn_settings is not None
    """


def test_set_remote_source_settings_to_tfs():
    """
    project_name = "tfs_test"
    projects_api = ProjectsAPI()
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
                                                                                              team_full_name)
    username = "dm\\tfs"
    absolute_url = "http://tfs2013/tfs/DefaultCollection"
    port = 8080
    paths = [
        "/Checkmarx/Optimisation/Checkmarx-V6.2.2.9-branch/CSharp/Graph"
    ]

    is_successful = projects_api.set_remote_source_settings_to_tfs(project_id, username, "", absolute_url, port,
                                                                   paths)
    assert is_successful is True
    """


def test_get_remote_source_settings_for_tfs_by_project_id():
    """
    project_name = "tfs_test"
    projects_api = ProjectsAPI()
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
                                                                                              team_full_name)
    tfs_settings = projects_api.get_remote_source_settings_for_tfs_by_project_id(project_id)
    assert tfs_settings is not None
    """


def test_set_remote_source_setting_for_custom_by_project_id():
    pass
    # project_name = "JVL-source-pulling"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
    #                                                                                           team_full_name)
    # path = ''
    # # Path should not be local
    # custom_task_name = "git"
    # custom_tasks_api = CustomTasksAPI()
    # pre_scan_command_id = custom_tasks_api.get_custom_task_id_by_name(custom_task_name)
    #
    # username = ''
    # result = projects_api.set_remote_source_setting_for_custom_by_project_id(project_id, path,
    #                                                                          pre_scan_command_id, username, '')
    # assert result is True


def test_get_remote_source_settings_for_custom_by_project_id():
    pass
    # project_name = "JVL-source-pulling"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    # custom_source_setting = projects_api.get_remote_source_settings_for_custom_by_project_id(project_id)
    # assert custom_source_setting is not None


def test_set_remote_source_settings_to_shared():
    pass
    # project_name = "jvl-shared"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
    #                                                                                           team_full_name)
    #
    # paths = [r'\\WIN-4MUJCQQ4KNT\Users\Administrator\Downloads\CxShare\JavaVulnerableLab-master']
    #
    # username = r"\\WIN-4MUJCQQ4KNT\Administrator"
    # result = projects_api.set_remote_source_settings_to_shared(project_id, paths, username, '')
    # assert result is True


def test_get_remote_source_settings_for_shared_by_project_id():
    pass
    # project_name = "jvl-shared"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    #
    # shared_source_setting = projects_api.get_remote_source_settings_for_shared_by_project_id(project_id)
    # assert shared_source_setting is not None


def test_set_remote_source_settings_to_perforce():
    pass
    # project_name = "perforce_test"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
    #                                                                                           team_full_name)
    #
    # username = "cx"
    # absolute_url = "10.32.0.75"
    # port = 1666
    # paths = ["//Depot_1/BookStore Java_21412lines/"]
    # browse_mode = "depot"
    #
    # is_successful = projects_api.set_remote_source_settings_to_perforce(project_id, username, '', absolute_url,
    #                                                                     port, paths, browse_mode)
    # assert is_successful is True


def test_get_remote_source_settings_for_perforce_by_project_id():
    pass
    # project_name = "perforce_test"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
    #                                                                                           team_full_name)
    #
    # perforce_settings = projects_api.get_remote_source_settings_for_perforce_by_project_id(project_id)
    # assert perforce_settings is not None


def test_set_remote_source_setting_to_git_using_ssh():
    project_name = "git-ssh"
    projects_api = ProjectsAPI()
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
                                                                                              team_full_name)

    url = "git@github.com:HappyY19/Cx-REST-API-SDK-Python.git"
    branch = "refs/heads/master"
    private_key_file_path = r"C:\Users\HappyY\.ssh\id_ed25519"
    result = projects_api.set_remote_source_setting_to_git_using_ssh(project_id, url, branch, private_key_file_path)
    assert result is True


def test_set_remote_source_setting_to_svn_using_ssh():
    pass
    # project_name = "svn-ssh"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
    #                                                                                           team_full_name)
    #
    # absolute_url = "svn+ssh://cx@10.32.3.91/testrepo"
    # port = 3690
    # paths = ["/"]
    # private_key_file_path = r"C:\Users\HappyY\Documents\Checkmarx\CxSAST\RD\svnSshKey"
    # is_successful = projects_api.set_remote_source_setting_to_svn_using_ssh(project_id, absolute_url, port,
    #                                                                         paths, private_key_file_path)
    # assert is_successful is True


def test_upload_source_code_zip_file():
    project_name = "JVL_local_zip"
    projects_api = ProjectsAPI()
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name,
                                                                                              team_full_name)

    file_name = "../../JavaVulnerableLab-master.zip"
    zip_file_path = normpath(join(dirname(__file__), file_name))
    result = projects_api.upload_source_code_zip_file(project_id, zip_file_path)
    assert result is True


def test_set_data_retention_settings_by_project_id():
    project_name = "JVL_local_zip"
    projects_api = ProjectsAPI()
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)

    result = projects_api.set_data_retention_settings_by_project_id(project_id, 20)
    assert result is True


def test_set_issue_tracking_system_as_jira_by_id():
    pass
    # project_name = "JVL_local_zip"
    # projects_api = ProjectsAPI()
    # project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    #
    # issue_tracking_system_id = 1
    # jira_project_id = None
    # issue_type_id = None
    # jira_fields = None
    #
    # is_successful = projects_api.set_issue_tracking_system_as_jira_by_id(project_id, issue_tracking_system_id,
    #                                                                      jira_project_id, issue_type_id, jira_fields)
    # assert is_successful is True


def test_get_all_preset_details():
    projects_api = ProjectsAPI()
    all_preset_details = projects_api.get_all_preset_details()
    assert all_preset_details is not None
    assert len(all_preset_details) > 0


def test_get_preset_id_by_name():
    projects_api = ProjectsAPI()
    preset_name = "Checkmarx Default"
    preset_id = projects_api.get_preset_id_by_name(preset_name)
    assert preset_id is not None


def test_get_preset_details_by_preset_id():
    projects_api = ProjectsAPI()
    preset_name = "Checkmarx Default"
    preset_id = projects_api.get_preset_id_by_name(preset_name)
    preset = projects_api.get_preset_details_by_preset_id(preset_id)
    assert preset is not None


def test_set_project_queue_setting():
    project_name = "jvl_git"
    projects_api = ProjectsAPI()
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    is_successful = projects_api.set_project_queue_setting(
        project_id=project_id, queue_keep_mode="KeepAll", scans_type="OnlyFull",
        include_scans_in_process=False, identical_code_only=False)
    assert is_successful is True


def test_update_project_queue_setting():
    project_name = "jvl_git"
    projects_api = ProjectsAPI()
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    is_successful = projects_api.update_project_queue_setting(
        project_id=project_id, queue_keep_mode="KeepAll", scans_type="OnlyFull",
        include_scans_in_process=False, identical_code_only=False)
    assert is_successful is True


def test_set_project_next_scheduled_scan_to_be_excluded_from_no_code_change_detection():
    project_name = "jvl_git"
    projects_api = ProjectsAPI()
    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team_full_name)
    is_successful = projects_api.set_project_next_scheduled_scan_to_be_excluded_from_no_code_change_detection(project_id)
    assert is_successful is True


def test_precheck_team():
    projects_api = ProjectsAPI()
    result = projects_api.precheck_team(1)
    assert result is not None

