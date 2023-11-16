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
    get_scan_reports,
    AccessControlAPI,
    get_aggregated_risks,
    get_artifact_license,
    get_artifact_info,
    get_suggest_private_package,
    execute_action_on_package_vulnerabilities,
    evaluate_package_vulnerabilities,
    disable_an_action_of_package_vulnerability,
    get_changes_of_package_vulnerabilities_of_a_project,
    search_entity_profile_of_package_vulnerabilities,
    execute_actions_on_supply_chain_risks,
    evaluate_supply_chain_risks,
    disable_an_action_for_a_supply_chain_risk,
    get_changes_of_supply_chain_risk,
    search_entity_profile_of_package_supply_chain_risks,
    execute_actions_on_package_license,
    evaluate_package_licenses,
    search_entity_profiles_of_package_licenses,
)
# from CheckmarxPythonSDK.CxScaApiSDK.AccessControlAPI import AccessControlAPI
project_name = "test_sca_2023_01_30"


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


def test_get_scan_reports():
    import time
    scan_id = "d5b2b7b4-a3d0-454b-b7ae-43de69d750db"

    # scan report
    json_report = get_scan_reports(scan_id=scan_id)
    with open("sca_scan_report.json", "wb") as json_file:
        json_file.write(json_report)
    time.sleep(5)
    xml_report = get_scan_reports(scan_id=scan_id, report_format="Xml")
    with open("sca_scan_report.xml", "wb") as xml_file:
        xml_file.write(xml_report)
    time.sleep(5)
    pdf_report = get_scan_reports(scan_id=scan_id, report_format="Pdf")
    with open("sca_scan_report.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_report)
    time.sleep(5)
    csv_report = get_scan_reports(scan_id=scan_id, report_format="Csv")
    with open("sca_scan_report.zip", "wb") as csv_zip:
        csv_zip.write(csv_report)
    time.sleep(5)
    # SBOM report
    sbom_report_in_json = get_scan_reports(scan_id=scan_id, report_format="CycloneDxJson")
    with open("sca_scan_sbom_report.json", "wb") as sbom_report_json_file:
        sbom_report_json_file.write(sbom_report_in_json)
    time.sleep(5)
    sbom_report_in_xml = get_scan_reports(scan_id=scan_id, report_format="CycloneDxXml")
    with open("sca_scan_sbom_report.xml", "wb") as sbom_report_xml_file:
        sbom_report_xml_file.write(sbom_report_in_xml)
    time.sleep(5)
    # scan report only with Vulnerabilities and Packages
    partial_json_report = get_scan_reports(scan_id=scan_id, data_types=("Vulnerabilities", "Packages"))
    with open("partial_sca_scan_report.json", "wb") as partial_json_file:
        partial_json_file.write(partial_json_report)
    time.sleep(5)
    partial_xml_report = get_scan_reports(scan_id=scan_id, report_format="Xml",
                                          data_types=("Vulnerabilities", "Packages"))
    with open("partial_sca_scan_report.xml", "wb") as partial_xml_file:
        partial_xml_file.write(partial_xml_report)
    time.sleep(5)
    partial_pdf_report = get_scan_reports(scan_id=scan_id, report_format="Pdf",
                                          data_types=("Vulnerabilities", "Packages"))
    with open("partial_sca_scan_report.pdf", "wb") as partial_pdf_file:
        partial_pdf_file.write(partial_pdf_report)
    time.sleep(5)
    partial_csv_report = get_scan_reports(scan_id=scan_id, report_format="Csv",
                                          data_types=("Vulnerabilities", "Packages"))
    with open("partial_sca_scan_report.zip", "wb") as partial_csv_zip_file:
        partial_csv_zip_file.write(partial_csv_report)
    assert partial_csv_report is not None


def test_get_aggregated_risks():
    resp = get_aggregated_risks("Python", "urllib3", "1.20")
    assert resp is not None


def test_get_artifact_license():
    resp = get_artifact_license("Python", "urllib3", "1.20")
    assert resp is not None


def test_get_artifact_info():
    resp = get_artifact_info("Python", "urllib3", "1.20")
    assert resp is not None


def test_get_suggest_private_package():
    resp = get_suggest_private_package("Python", "nltk", "3.8.1")
    assert resp is not None


def test_execute_action_on_package_vulnerabilities():
    package_name = "org.apache.tomcat.embed:tomcat-embed-core"
    package_manager = "maven"
    vulnerability_id = "CVE-2022-42252"
    package_version = "9.0.46"
    project_ids = ["6413c96c-b19e-4f4e-82bf-e637fa011c18"]
    actions = [
        {
            "actionType": "ChangeState",
            "value": "Confirmed",
            "comment": "Change State to Confirmed"
        }
    ]

    resp = execute_action_on_package_vulnerabilities(package_name, package_manager, vulnerability_id, package_version,
                                                     project_ids, actions)
    assert resp is not None


def test_evaluate_package_vulnerabilities():
    scan_id = ""
    entities = []
    resp = evaluate_package_vulnerabilities(scan_id, entities)
    assert resp is not None


def test_disable_an_action_of_package_vulnerability():
    package_name = ""
    package_version = ""
    package_manager = ""
    vulnerability_id = ""
    project_ids = []
    action_type = ""
    resp = disable_an_action_of_package_vulnerability(package_name, package_version, package_manager, vulnerability_id,
                                                      project_ids, action_type)
    assert resp is not None


def test_get_changes_of_package_vulnerabilities_of_a_project():
    project_id = ""
    from_when = ""
    skip = 0
    take = 100
    resp = get_changes_of_package_vulnerabilities_of_a_project(project_id, from_when, skip, take)
    assert resp is not None


def test_search_entity_profile_of_package_vulnerabilities():
    package_name = ""
    package_version = ""
    package_manager = ""
    vulnerability_id = ""
    project_id = ""
    action_type = ""
    to_when = ""
    resp = search_entity_profile_of_package_vulnerabilities(package_name, package_version, package_manager, vulnerability_id,
                                                     project_id, action_type, to_when)
    assert resp is not None


def test_execute_actions_on_supply_chain_risks():
    package_name = ""
    package_manager = ""
    supply_chain_risk_id = ""
    package_version = ""
    project_ids = ""
    actions = []
    resp = execute_actions_on_supply_chain_risks(package_name, package_manager, supply_chain_risk_id, package_version,
                                                 project_ids, actions)
    assert resp is not None


def test_evaluate_supply_chain_risks():
    scan_id = ""
    entities = []
    resp = evaluate_supply_chain_risks(scan_id, entities)
    assert resp is not None


def test_disable_an_action_for_a_supply_chain_risk():
    package_name = ""
    package_version = ""
    package_manager = ""
    supply_chain_risk_id = ""
    project_ids = []
    action_type = ""
    resp = disable_an_action_for_a_supply_chain_risk(package_name, package_version, package_manager,
                                                     supply_chain_risk_id,
                                              project_ids, action_type)
    assert resp is not None


def test_get_changes_of_supply_chain_risk():
    project_id = ""
    from_when = ""
    skip = 0
    take = 100
    resp = get_changes_of_supply_chain_risk(project_id, from_when, skip, take)
    assert resp is not None


def test_search_entity_profile_of_package_supply_chain_risks():
    package_name = ""
    package_version = ""
    package_manager = ""
    supply_chain_risk_id = ""
    project_id = ""
    action_type = ""
    to_when = ""
    resp = search_entity_profile_of_package_supply_chain_risks(package_name, package_version, package_manager,
                                                        supply_chain_risk_id, project_id, action_type, to_when)
    assert resp is not None


def test_execute_actions_on_package_license():
    package_id = ""
    license_name = ""
    project_ids = []
    actions = []
    resp = execute_actions_on_package_license(package_id, license_name, project_ids, actions)
    assert resp is not None


def test_evaluate_package_licenses():
    entities = []
    scan_id = ""
    resp = evaluate_package_licenses(entities, scan_id)
    assert resp is not None


def test_search_entity_profiles_of_package_licenses():
    package_id = ""
    license_name = ""
    project_id = ""
    action_type = ""
    to_when = ""
    resp = search_entity_profiles_of_package_licenses(package_id, license_name, project_id, action_type, to_when)
    assert resp is not None
