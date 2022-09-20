from CheckmarxPythonSDK.CxRestAPISDK.ProjectsAPI import ProjectsAPI


def get_project_id(project_name="jvl_git"):
    projects_api = ProjectsAPI()
    project_name = project_name
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(
        project_name, "/CxServer"
    )

    return project_id
