# encoding: utf-8

import time

from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI


def get_project_id(project_name="jvl_git"):
    projects_api = ProjectsAPI()
    project_name = project_name
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name)

    return project_id


def test_create_new_scan():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan = scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                                    comment="scan from REST API")
    time.sleep(300)
    assert scan is not None


def test_get_all_scans_for_project():
    project_id = get_project_id()

    scan_api = ScansAPI()
    all_scans = scan_api.get_all_scans_for_project(project_id)
    assert all_scans is not None


def test_get_last_scan_id_of_a_project():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id)
    assert scan_id is not None


def test_get_sast_scan_details_by_scan_id():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id)
    scan = scan_api.get_sast_scan_details_by_scan_id(scan_id)
    assert scan is not None


def test_add_or_update_a_comment_by_scan_id():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    result = scan_api.add_or_update_a_comment_by_scan_id(scan_id, "updated scan")
    assert result is True


def test_delete_scan_by_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    result = scan_api.delete_scan_by_scan_id(scan_id)
    assert result is True


def test_get_statistics_results_by_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    statistics = scan_api.get_statistics_results_by_scan_id(scan_id)
    assert statistics is not None


def test_get_scan_queue_details_by_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                             comment="scan from REST API")
    time.sleep(5)
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id)
    scan_queue_details = scan_api.get_scan_queue_details_by_scan_id(scan_id)
    assert scan_queue_details is not None


def test_update_queued_scan_status_by_scan_id():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan = scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                                    comment="scan from REST API")
    time.sleep(5)
    result = scan_api.update_queued_scan_status_by_scan_id(scan_id=scan.id)
    assert result is True
    # TODO  check  why not can't deserialize scanRequest.status.id


def test_get_all_scan_details_in_queue():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                             comment="scan from REST API")
    time.sleep(4)
    all_scan_details_in_queue = scan_api.get_all_scan_details_in_queue()
    assert all_scan_details_in_queue is not None


def test_get_scan_settings_by_project_id():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_settings = scan_api.get_scan_settings_by_project_id(project_id)
    assert scan_settings is not None


def test_define_sast_scan_settings():
    project_id = get_project_id()

    scan_api = ScansAPI()
    project_api = ProjectsAPI()
    preset_id = project_api.get_preset_id_by_name("Checkmarx Default")
    engine_configuration_id = 1
    post_scan_action_id = None
    failed_scan_emails = ["test@checkmarx.com"]
    before_scan_emails = ["test@checkmarx.com"]
    after_scan_emails = ["test@checkmarx.com"]
    scan_setting = scan_api.define_sast_scan_settings(project_id, preset_id, engine_configuration_id,
                                                      post_scan_action_id,
                                                      failed_scan_emails, before_scan_emails, after_scan_emails)
    assert scan_setting is not None


def test_update_sast_scan_settings():
    project_id = get_project_id()
    scan_api = ScansAPI()
    project_api = ProjectsAPI()
    preset_id = project_api.get_preset_id_by_name("Checkmarx Default")
    engine_configuration_id = 1
    post_scan_action_id = None
    failed_scan_emails = ["test@checkmarx.com"]
    before_scan_emails = ["test@checkmarx.com"]
    after_scan_emails = ["test@checkmarx.com"]
    scan_settings = scan_api.update_sast_scan_settings(project_id, preset_id, engine_configuration_id,
                                                       post_scan_action_id,
                                                       failed_scan_emails, before_scan_emails, after_scan_emails)
    assert scan_settings is not None


def test_define_sast_scan_scheduling_settings():
    project_id = get_project_id()

    scan_api = ScansAPI()
    schedule_type = "weekly"
    schedule_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule_time = "23:59"
    result = scan_api.define_sast_scan_scheduling_settings(project_id, schedule_type, schedule_days, schedule_time)
    assert result is True


# def test_assign_ticket_to_scan_results():
#     scan_api = ScansAPI()
#
#     results_id = None
#     ticket_id = None
#     is_successful = scan_api.assign_ticket_to_scan_results(results_id, ticket_id)
#     assert is_successful is True
#     pass
#     # TODO, need to parse XML file to get resultId
#
#
# def test_publish_last_scan_results_to_management_and_orchestration_by_project_id():
#     project_id = get_project_id()
#     scan_api = ScansAPI()
#     policy_finding_response = scan_api.publish_last_scan_results_to_management_and_orchestration_by_project_id(
#         project_id)
#     assert policy_finding_response is not None
#
#
# def test_get_the_publish_last_scan_results_to_management_and_orchestration_status():
#     project_id = get_project_id()
#     scan_api = ScansAPI()
#     policy_finding_status = scan_api.get_the_publish_last_scan_results_to_management_and_orchestration_status(
#         project_id)
#     assert policy_finding_status is not None


def test_get_short_vulnerability_description_for_a_scan_result():
    """
    This test may raise error:
    NotFoundError(http_code=404, msg="Result path Id 1 does not exist for scan with Id 1000020")
    """
    path_id = 1
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    short_description = scan_api.get_short_vulnerability_description_for_a_scan_result(scan_id=scan_id, path_id=path_id)
    assert short_description is not None


def test_register_scan_report():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    report_type = "XML"
    scan_report = scan_api.register_scan_report(scan_id, report_type)
    assert scan_report is not None

    report_id = scan_report.report_id
    report_status = scan_api.get_report_status_by_id(report_id)
    assert report_status is not None
    time.sleep(30)
    report_content = scan_api.get_report_by_id(report_id)
    assert report_content is not None
