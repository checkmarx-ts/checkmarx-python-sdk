"""
1. get token (auth header)
2. get team id
3. create project with default configuration, will get project id
4. upload source code zip file
5[optional]. set issue tracking system as jira by id
6[optional]. set data retention settings by project id
7. define SAST scan settings, set preset, engine configuration
8. create new scan, will get a scan id
9. get scan details by scan id
10[optional]. get scan queue details by scan id
11[optional]. get statistics results by scan id
12. register scan report
13. get report status by id
14. get report by id
"""

import time

from pathlib import Path

from CxRestAPISDK import TeamAPI
from CxRestAPISDK import ProjectsAPI
from CxRestAPISDK import ScansAPI


def check_scan_finished(scan_id):
    is_finished = False
    scan_api = ScansAPI()
    scan_detail = scan_api.get_sast_scan_details_by_scan_id(scan_id=scan_id)
    if scan_detail.status.name == "Finished":
        is_finished = True
    return is_finished


def check_report_generation_finished(report_id):
    is_finished = False
    scan_api = ScansAPI()
    report_status = scan_api.get_report_status_by_id(report_id)
    if report_status.status.value == "Created":
        is_finished = True
    return is_finished


def get_project_id_by_name(project_name, team_name="/CxServer/SP/Company/Users"):
    projects_api = ProjectsAPI()
    team_api = TeamAPI()
    team_id = team_api.get_team_id_by_full_name()
    if team_name != "/CxServer/SP/Company/Users":
        team_id = team_api.get_team_id_by_full_name(team_name)
    project_id = projects_api.get_project_id_by_name(project_name, team_id)
    return project_id


def delete_project_if_exists(project_name):
    result = False
    projects_api = ProjectsAPI()
    project_id = get_project_id_by_name(project_name, "/CxServer")
    if project_id:
        result = projects_api.delete_project_by_id(project_id)
    return result


def scan_from_local():

    # 2. get team id
    team_id = TeamAPI().get_team_id_by_full_name("/CxServer")
    projects_api = ProjectsAPI()
    project_name = "jvl_local"
    delete_project_if_exists(project_name)

    # 3. create project with default configuration, will get project id
    project = projects_api.create_project_with_default_configuration(name=project_name, owning_team=team_id)
    project_id = project.id

    # 4. upload source code zip file
    zip_file_path = Path(__file__).parent.absolute() / "JavaVulnerableLab-master.zip"
    projects_api.upload_source_code_zip_file(project_id, str(zip_file_path))

    # 6. set data retention settings by project id
    projects_api.set_data_retention_settings_by_project_id(project_id=project_id, scans_to_keep=3)
    scan_api = ScansAPI()

    # 7. define SAST scan settings
    scan_api.define_sast_scan_settings(project_id=project_id)

    # 8. create new scan, will get a scan id
    scan = scan_api.create_new_scan(project_id=project_id)
    scan_id = scan.id

    # 9. get scan details by scan id
    while not check_scan_finished(scan_id):
        time.sleep(1)

    # 11[optional]. get statistics results by scan id
    statistics = scan_api.get_statistics_results_by_scan_id(scan_id=scan_id)
    if statistics:
        print(statistics)

    # 12. register scan report
    report = scan_api.register_scan_report(scan_id=scan_id, report_type="XML")
    report_id = report.report_id

    # 13. get report status by id
    while not check_report_generation_finished(report_id):
        time.sleep(1)

    # 14. get report by id
    report_content = scan_api.get_report_by_id(report_id)

    file_name = Path(__file__).parent.absolute() / "local_report.xml"
    with open(str(file_name), "wb") as file:
        file.write(report_content)


if __name__ == "__main__":
    scan_from_local()
