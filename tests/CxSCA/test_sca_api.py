from CheckmarxPythonSDK.CxScaApiSDK import (
    get_all_projects,
    check_if_project_already_exists,
    create_a_new_project,
    get_project_id_by_name,
    get_project_by_id,
    update_project,
    delete_project,
    get_all_scans_associated_with_a_project,
    get_latest_scan_id_of_a_project,
    get_scan_by_id,
    get_scan_status,
    get_scan_settings,
    get_risk_report_summary,
    get_packages_of_a_scan,
    get_vulnerabilities_of_a_scan,
    get_licenses_of_a_scan,
    ignore_a_vulnerability_for_a_specific_package_and_project,
    undo_the_ignore_state_of_an_ignored_vulnerability,
    get_settings_for_a_specific_project,
    update_settings_for_a_specific_project,
    generate_upload_link_for_scanning,
    upload_zip_content_for_scanning,
    scan_previously_uploaded_zip,
    get_comments_associated_with_a_project,
    comment_a_vulnerability_for_a_specific_package_and_project,
    get_states_associated_with_a_project,
    change_state_of_a_vulnerability_for_a_specific_package_and_project,
    AccessControlAPI
)
# from CheckmarxPythonSDK.CxScaApiSDK.AccessControlAPI import AccessControlAPI
project_name = "test_sca_2021_01_18"


def test_get_all_projects():
    all_projects = get_all_projects()
    assert len(all_projects) > 0


def test_check_if_project_already_exists():
    another_project_name = "happy_test_2021_01_15_not_exist"
    exist_status = check_if_project_already_exists(another_project_name)
    assert exist_status is False


def test_create_a_new_project():
    project = create_a_new_project(project_name=project_name)
    assert project.get("id") is not None


def test_get_project_by_name():
    project = get_all_projects(project_name=project_name)
    assert project is not None


def test_get_project_id_by_name():
    project_id = get_project_id_by_name(project_name)
    assert isinstance(project_id, str)
    project_id = get_project_id_by_name(['Sample App', 'Test Project'])
    assert isinstance(project_id, list)


def test_get_project_by_id():
    project_id = get_project_id_by_name(project_name)
    project = get_project_by_id(project_id=project_id)
    assert project is not None


def test_update_project():
    project_id = get_project_id_by_name(project_name)
    is_successful = update_project(project_id=project_id, project_name="happy_test_2021_01_14_2",
                                   assigned_teams=["/CxServer/SCA-PM/Champions/UK"])
    assert is_successful is True


def test_delete_project():
    project_id = get_project_id_by_name(project_name)
    is_successful = delete_project(project_id=project_id)
    assert is_successful is True


def test_get_all_scans_associated_with_a_project():
    project_id = get_project_id_by_name(project_name)
    scans = get_all_scans_associated_with_a_project(project_id=project_id)
    assert len(scans) == 0


def test_get_latest_scan_id_of_a_project():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    assert scan_id is not None


def test_get_scan_by_id():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    scan = get_scan_by_id(scan_id=scan_id)
    assert scan is not None


def test_get_scan_status():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    scan_status = get_scan_status(scan_id=scan_id)
    assert scan_status is not None


def test_get_scan_settings():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    scan_settings = get_scan_settings(scan_id=scan_id)
    assert scan_settings is not None


def test_get_risk_report_summary():
    project_id = get_project_id_by_name(project_name)
    risk_report_summary = get_risk_report_summary(project_id=project_id)
    assert risk_report_summary is not None


def test_get_packages_of_a_scan():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    packages = get_packages_of_a_scan(scan_id=scan_id)
    assert len(packages) > 0


def test_get_vulnerabilities_of_a_scan():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    vulnerabilities = get_vulnerabilities_of_a_scan(scan_id=scan_id)
    assert len(vulnerabilities) > 0


def test_get_licenses_of_a_scan():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    licenses = get_licenses_of_a_scan(scan_id=scan_id)
    assert len(licenses) > 0


def test_ignore_a_vulnerability_for_a_specific_package_and_project():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    vulnerabilities = get_vulnerabilities_of_a_scan(scan_id=scan_id)
    vulnerability_id = vulnerabilities[0].get("id")
    packages = get_packages_of_a_scan(scan_id=scan_id)
    package_id = packages[0].get("id")

    is_successful = ignore_a_vulnerability_for_a_specific_package_and_project(
        project_id=project_id,
        vulnerability_id=vulnerability_id,
        package_id=package_id
    )
    assert is_successful is True


def test_undo_the_ignore_state_of_an_ignored_vulnerability():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    vulnerabilities = get_vulnerabilities_of_a_scan(scan_id=scan_id)
    vulnerability_id = vulnerabilities[0].get("id")
    packages = get_packages_of_a_scan(scan_id=scan_id)
    package_id = packages[0].get("id")
    is_successful = undo_the_ignore_state_of_an_ignored_vulnerability(
        project_id=project_id,
        vulnerability_id=vulnerability_id,
        package_id=package_id
    )
    assert is_successful is True


def test_get_settings_for_a_specific_project():
    project_id = get_project_id_by_name(project_name)
    project_settings = get_settings_for_a_specific_project(project_id=project_id)
    assert project_settings is not None


# not passed
def test_update_settings_for_a_specific_project():
    project_id = get_project_id_by_name(project_name)
    is_successful = update_settings_for_a_specific_project(project_id=project_id, enable_exploitable_path=True)
    assert is_successful is True


def test_generate_upload_link_for_scanning():
    project_id = get_project_id_by_name(project_name)
    upload_link = generate_upload_link_for_scanning(project_id=project_id)
    assert upload_link is not None
    zip_file_path = "../JavaVulnerableLab-master.zip"
    is_successful = upload_zip_content_for_scanning(upload_link, zip_file_path)
    assert is_successful is True
    scan_id = scan_previously_uploaded_zip(project_id=project_id, uploaded_file_url=upload_link)
    assert scan_id is not None


def test_get_comments_associated_with_a_project():
    project_id = get_project_id_by_name(project_name)
    project_comments = get_comments_associated_with_a_project(project_id)
    assert project_comments is not None


def test_comment_a_vulnerability_for_a_specific_package_and_project():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    vulnerabilities = get_vulnerabilities_of_a_scan(scan_id=scan_id)
    vulnerability_id = vulnerabilities[0].get("id")
    packages = get_packages_of_a_scan(scan_id=scan_id)
    package_id = packages[0].get("id")
    is_successful = comment_a_vulnerability_for_a_specific_package_and_project(
        project_id=project_id,
        vulnerability_id=vulnerability_id,
        package_id=package_id,
        comment="test_SDK"
    )
    assert is_successful is True


def test_get_states_associated_with_a_project():
    project_id = get_project_id_by_name(project_name)
    project_states = get_states_associated_with_a_project(project_id)
    assert project_states is not None


def test_change_state_of_a_vulnerability_for_a_specific_package_and_project():
    project_id = get_project_id_by_name(project_name)
    scan_id = get_latest_scan_id_of_a_project(project_id=project_id)
    vulnerabilities = get_vulnerabilities_of_a_scan(scan_id=scan_id)
    vulnerability_id = vulnerabilities[0].get("id")
    packages = get_packages_of_a_scan(scan_id=scan_id)
    package_id = packages[0].get("id")
    is_successful = change_state_of_a_vulnerability_for_a_specific_package_and_project(
        project_id=project_id,
        vulnerability_id=vulnerability_id,
        package_id=package_id,
        state="NotExploitable"
    )
    assert is_successful is True
