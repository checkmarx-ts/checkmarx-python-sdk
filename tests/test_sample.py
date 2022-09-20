from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI


def test_sample():
    team_api = TeamAPI()
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()

    team_id = team_api.get_team_id_by_team_full_name("/CxServer")
    projects = projects_api.get_all_project_details(project_name="jvl_git", team_id=team_id)

    for project in projects:
        scans = scan_api.get_all_scans_for_project(project_id=project.project_id, scan_status='Finished')

        for scan in scans:
            print(str(scan.id))


test_sample()
