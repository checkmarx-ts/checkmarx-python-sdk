"""
1. get token (auth header)
2. get team id
3. create project with default configuration, will get project id
4. set remote source setting to git
5[optional]. set issue tracking system as jira by id
6. set data retention settings by project id
7. define SAST scan settings
8. create new scan, will get a scan id
9. get scan details by scan id
10[optional]: get scan queue details by scan id
11[optional]. get statistics results by scan id
12. register scan report
13. get report status by id
14. get report by id
15[optional]. filter report results
"""
import time
from os.path import normpath, join, dirname
from datetime import datetime
from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI


def scan_from_git():
    team_full_name = "/CxServer"
    project_name = "jvl_git"
    report_type = "PDF"
    url = "https://github.com/CSPF-Founder/JavaVulnerableLab.git"
    branch = "refs/heads/master"

    projects_api = ProjectsAPI()
    team_api = TeamAPI()
    scan_api = ScansAPI()

    # 2. get team id
    print("2. get team id")
    team_id = team_api.get_team_id_by_team_full_name(team_full_name)
    if not team_id:
        print("team: {} not exist".format(team_full_name))
        return

    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name=project_name,
                                                                                team_full_name=team_full_name)

    # 3. create project with default configuration, will get project id
    print("3. create project with default configuration, will get project id")
    if not project_id:
        project = projects_api.create_project_with_default_configuration(project_name=project_name, team_id=team_id)
        project_id = project.id
    print("project_id: {}".format(project_id))

    # 4. set remote source setting to git
    print("4. set remote source setting to git")
    projects_api.set_remote_source_setting_to_git(project_id=project_id, url=url, branch=branch)

    # 6. set data retention settings by project id
    print("6. set data retention settings by project id")
    projects_api.set_data_retention_settings_by_project_id(project_id=project_id, scans_to_keep=3)

    # 7. define SAST scan settings
    print("7. define SAST scan settings")
    preset_id = projects_api.get_preset_id_by_name()
    print("preset id: {}".format(preset_id))
    scan_api.define_sast_scan_settings(project_id=project_id, preset_id=preset_id)

    projects_api.set_project_exclude_settings_by_project_id(project_id, exclude_folders_pattern="",
                                                            exclude_files_pattern="")

    # 8. create new scan, will get a scan id
    print("8. create new scan, will get a scan id")
    scan = scan_api.create_new_scan(project_id=project_id)
    scan_id = scan.id
    print("scan_id : {}".format(scan_id))

    # 9. get scan details by scan id
    print("9. get scan details by scan id")
    while True:
        scan_detail = scan_api.get_sast_scan_details_by_scan_id(scan_id=scan_id)
        scan_status = scan_detail.status.name
        print("scan_status: {}".format(scan_status))
        if scan_status == "Finished":
            break
        elif scan_status == "Failed":
            return
        time.sleep(10)

    # 11[optional]. get statistics results by scan id
    print("11[optional]. get statistics results by scan id")
    statistics = scan_api.get_statistics_results_by_scan_id(scan_id=scan_id)
    if statistics:
        print(statistics)

    # 12. register scan report
    print("12. register scan report")
    report = scan_api.register_scan_report(scan_id=scan_id, report_type=report_type)
    report_id = report.report_id
    print("report_id : {}".format(report_id))

    # 13. get report status by id
    print("13. get report status by id")
    while not scan_api.is_report_generation_finished(report_id):
        time.sleep(10)

    # 14. get report by id
    print("14. get report by id")
    report_content = scan_api.get_report_by_id(report_id)
    time_stamp = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
    file_name = normpath(join(dirname(__file__), project_name + time_stamp + "." + report_type))
    with open(str(file_name), "wb") as f_out:
        f_out.write(report_content)


if __name__ == "__main__":
    scan_from_git()
