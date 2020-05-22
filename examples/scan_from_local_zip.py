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
import io
from pathlib import Path

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.CxRestAPISDK.sast.scans.dto.CxScanReportXmlContent import CxScanReportXmlContent


def scan_from_local():

    team_full_name = "/CxServer"
    project_name = "jvl_local"
    zip_file_path = Path(__file__).parent.absolute() / "JavaVulnerableLab-master.zip"
    report_name = "local_report.xml"
    filter_xml = True

    team_api = TeamAPI()
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()

    projects_api.delete_project_if_exists_by_project_name_and_team_full_name(project_name, team_full_name)

    # 2. get team id
    print("2. get team id")
    team_id = team_api.get_team_id_by_team_full_name(team_full_name)

    # 3. create project with default configuration, will get project id
    print("3. create project with default configuration, will get project id")
    project = projects_api.create_project_with_default_configuration(project_name=project_name, team_id=team_id)
    project_id = project.id

    # 4. upload source code zip file
    print("4. upload source code zip file")
    projects_api.upload_source_code_zip_file(project_id, str(zip_file_path))

    # 6. set data retention settings by project id
    print("6. set data retention settings by project id")
    projects_api.set_data_retention_settings_by_project_id(project_id=project_id, scans_to_keep=3)

    # 7. define SAST scan settings
    print("7. define SAST scan settings")
    preset_id = projects_api.get_preset_id_by_name()
    scan_api.define_sast_scan_settings(project_id=project_id, preset_id=preset_id)

    # 8. create new scan, will get a scan id
    print("8. create new scan, will get a scan id")
    scan = scan_api.create_new_scan(project_id=project_id)
    scan_id = scan.id
    print("scan_id: {}".format(scan_id))

    # 9. get scan details by scan id
    print("9. get scan details by scan id")
    while True:
        scan_detail = scan_api.get_sast_scan_details_by_scan_id(scan_id=scan_id)
        scan_status = scan_detail.status.name
        if scan_status == "Finished":
            break
        elif scan_status == "Failed":
            return
        time.sleep(1)

    # 11[optional]. get statistics results by scan id
    print("11[optional]. get statistics results by scan id")
    statistics = scan_api.get_statistics_results_by_scan_id(scan_id=scan_id)
    if statistics:
        print(statistics)

    # 12. register scan report
    print("12. register scan report")
    report = scan_api.register_scan_report(scan_id=scan_id, report_type="XML")
    report_id = report.report_id
    print("report_id: {}".format(report_id))

    # 13. get report status by id
    print("13. get report status by id")
    while not scan_api.is_report_generation_finished(report_id):
        time.sleep(1)

    # 14. get report by id
    print("14. get report by id")
    report_content = scan_api.get_report_by_id(report_id)

    # optional, filter XML report data
    file_name = Path(__file__).parent.absolute() / "filter_by_severity.xml"
    if "xml" in report_name and filter_xml:
        f = io.BytesIO(report_content)
        xml_report = CxScanReportXmlContent(f)
        xml_report.filter_by_severity(high=True, medium=True)
        xml_report.write_new_xml(str(file_name))

    report_path = Path(__file__).parent.absolute() / report_name
    with open(str(report_path), "wb") as file:
        file.write(report_content)


if __name__ == "__main__":
    scan_from_local()
