"""
SCA scan example

"""
import json
import time
from datetime import datetime
from os.path import exists

from CheckmarxPythonSDK.CxScaApiSDK import (
    check_if_project_already_exists,
    create_a_new_project,
    get_project_id_by_name,
    generate_upload_link_for_scanning,
    upload_zip_content_for_scanning,
    scan_previously_uploaded_zip,
    get_scan_status,
    get_risk_report_summary,
    get_packages_of_a_scan,
    get_vulnerabilities_of_a_scan,
    get_licenses_of_a_scan,
)


def get_project_id(project_name):
    project_exists = check_if_project_already_exists(project_name)
    if not project_exists:
        project = create_a_new_project(project_name=project_name)
        return project.get("id")
    return get_project_id_by_name(project_name)


def sca_scan(project_name, zip_file_path):
    if not exists(zip_file_path):
        print("zip_file_path:{} not exists. \n abort scan.".format(zip_file_path))
        return

    project_id = get_project_id(project_name)
    print("project_id: {}".format(project_id))

    upload_link = generate_upload_link_for_scanning(project_id=project_id)
    is_successful = upload_zip_content_for_scanning(upload_link, zip_file_path)
    if not is_successful:
        print("Fail to upload file with upload link: {}  \n abort scan.".format(upload_link))
        return

    scan_id = scan_previously_uploaded_zip(project_id=project_id, uploaded_file_url=upload_link)
    print("scan_id: {}".format(scan_id))

    while True:
        response = get_scan_status(scan_id=scan_id)
        scan_status = response.get("name")
        if scan_status == "Scanning":
            print("scanning ...")
            continue
        elif scan_status == "Done":
            print("scan finished successfully!")
            break
        elif scan_status == "Failed":
            print("scan_status:{}, message:{}".format(scan_status, response.get("message")))
            return
        time.sleep(10)

    risk_report_summary = get_risk_report_summary(project_id=project_id)
    print("risk_report_summary:{}".format(risk_report_summary))

    packages = get_packages_of_a_scan(scan_id=scan_id)
    print("get packages of a scan")
    vulnerabilities = get_vulnerabilities_of_a_scan(scan_id=scan_id)
    print("get vulnerabilities of a scan")
    licenses = get_licenses_of_a_scan(scan_id=scan_id)
    print("get licenses of a scan")
    time_stamp = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
    print("create sca json report")
    with open("sca_report" + time_stamp + ".json", "w") as out_file:
        out_file.write(
            json.dumps(
                {
                    "project_name": project_name,
                    "project_id": project_id,
                    "scan_id": scan_id,
                    "risk_report_summary": risk_report_summary,
                    "packages": packages,
                    "vulnerabilities": vulnerabilities,
                    "licenses": licenses
                }, indent=4
            )
        )


if __name__ == "__main__":
    sca_project_name = "test_sca_2021_01_18"
    sca_zip_file_path = r"C:\Users\HappyY\Documents\SourceCode\GitHub\checkmarx-python-sdk\examples\JavaVulnerableLab-master.zip"
    sca_scan(sca_project_name, sca_zip_file_path)
