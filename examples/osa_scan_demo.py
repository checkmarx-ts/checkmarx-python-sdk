"""
This is a CxOSA scan demo
"""
import time
from pathlib import Path

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import OsaAPI

zip_file_path = Path(__file__).parent.absolute() / "JavaVulnerableLab-master.zip"


def osa_scan():
    team_full_name = "/CxServer"
    project_name = "OSA_demo"

    projects_api = ProjectsAPI()
    team_api = TeamAPI()
    osa_api = OsaAPI()

    # 1. create project
    projects_api.delete_project_if_exists_by_project_name_and_team_full_name(project_name, team_full_name)

    # 2. get team id
    team_id = team_api.get_team_id_by_team_full_name(team_full_name)

    # 3. create project with default configuration, will get project id
    project = projects_api.create_project_with_default_configuration(project_name=project_name, team_id=team_id)
    project_id = project.id

    # 4. create an OSA scan
    scan_id = osa_api.create_an_osa_scan_request(project_id=project_id, zipped_source_path=zip_file_path,
                                                 origin="REST API")

    # 5. check scan status
    while True:
        osa_scan_detail = osa_api.get_osa_scan_by_scan_id(scan_id)
        osa_scan_state = osa_scan_detail.state.name
        if osa_scan_state == "Succeeded":
            break
        elif osa_scan_state == "Failed":
            print("OSA scan failed")
            return
        else:
            time.sleep(1)

    # 6. get summary report
    summary_report = osa_api.get_osa_scan_summary_report(scan_id=scan_id)

    print(summary_report)


if __name__ == "__main__":
    osa_scan()
