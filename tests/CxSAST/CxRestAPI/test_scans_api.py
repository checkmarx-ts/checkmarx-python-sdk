"""
    tests.test_scans_api

    :copyright Checkmarx
    :license GPL-3

"""
import time
import pytest
from os.path import normpath, join, dirname
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_query_collection

from .. import get_project_id


def _get_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    return scan_api.get_last_scan_id_of_a_project(
        project_id,
        only_finished_scans=True,
        only_completed_scans=True,
        only_real_scans=True,
        only_full_scans=True,
    )


def _get_query_version_code():
    result = get_query_collection()
    for qg in result.get("QueryGroups", []):
        if qg.get("LanguageName") == "Java":
            for q in qg.get("Queries") or []:
                if q.get("Name") == "SQL_Injection":
                    return q.get("QueryVersionCode")
    return None


def test_create_new_scan():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                             comment="scan from REST API")
    time.sleep(30)
    scan = scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                                    custom_fields={"key1": "value1", "key2": "value2"},
                                    comment="scan from Python SDK", api_version="1.2")
    scan_id = scan.id
    assert scan_id > 1


def test_get_all_scans_for_project():
    project_id = get_project_id()

    scan_api = ScansAPI()
    all_scans = scan_api.get_all_scans_for_project(project_id, api_version="1.2")
    assert len(all_scans) > 1

    last_ten_scans = scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Finished", last=10,
                                                        api_version="1.2")
    assert len(last_ten_scans) > 1

    last_ten_scans_api_1 = scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Finished", last=10)
    assert len(last_ten_scans_api_1) > 1

    scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Scanning", last=10)
    scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Canceled", last=10)
    scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Failed", last=10)


def test_get_last_scan_id_of_a_project():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True, only_completed_scans=True,
                                                     only_real_scans=True, only_full_scans=True)
    assert scan_id > 1


def test_get_sast_scan_details_by_scan_id():
    scan_id = _get_scan_id()
    scan = ScansAPI().get_sast_scan_details_by_scan_id(scan_id)
    assert scan is not None


def test_add_or_update_a_comment_by_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    result = scan_api.add_or_update_a_comment_by_scan_id(scan_id, "updated scan comment")
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
    scan = scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                                    comment="scan from REST API")
    time.sleep(5)
    try:
        scan_queue_details = scan_api.get_scan_queue_details_by_scan_id(scan.id)
        assert scan_queue_details is not None
    except ValueError:
        pytest.skip("Scan completed before queue details could be retrieved")


def test_update_queued_scan_status_by_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan = scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                                    comment="scan from REST API")
    time.sleep(5)
    result = scan_api.update_queued_scan_status_by_scan_id(scan_id=scan.id)
    assert result is True


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
    scan_setting = scan_api.define_sast_scan_settings(
        project_id, preset_id, engine_configuration_id, None,
        ["test@checkmarx.com"], ["test@checkmarx.com"], ["test@checkmarx.com"],
    )
    assert scan_setting is not None


def test_update_sast_scan_settings():
    project_id = get_project_id()
    scan_api = ScansAPI()
    project_api = ProjectsAPI()
    preset_id = project_api.get_preset_id_by_name("Checkmarx Default")
    engine_configuration_id = 1
    scan_settings = scan_api.update_sast_scan_settings(
        project_id, preset_id, engine_configuration_id, None,
        ["test@checkmarx.com"], ["test@checkmarx.com"], ["test@checkmarx.com"],
    )
    assert scan_settings is not None


def test_define_sast_scan_scheduling_settings():
    project_id = get_project_id()
    scan_api = ScansAPI()
    schedule_type = "weekly"
    schedule_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule_time = "23:59"
    result = scan_api.define_sast_scan_scheduling_settings(project_id, schedule_type, schedule_days, schedule_time)
    assert result is True


def test_get_short_vulnerability_description_for_a_scan_result():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    short_description = scan_api.get_short_vulnerability_description_for_a_scan_result(scan_id=scan_id, path_id=1)
    assert short_description is not None


def test_register_scan_report():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(
        project_id, only_finished_scans=True, only_completed_scans=False,
        only_real_scans=False, only_full_scans=False, only_public_scans=False,
    )
    report_type = "CSV"
    scan_report = scan_api.register_scan_report(scan_id, report_type)
    assert scan_report is not None

    report_id = scan_report.report_id
    report_status = scan_api.get_report_status_by_id(report_id)
    assert report_status is not None
    time.sleep(30)
    report_content = scan_api.get_report_by_id(report_id)
    assert report_content is not None
    with open("cx-report.csv", "wb") as f_out:
        f_out.write(report_content)


def test_get_scan_results_of_a_specific_query():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    query_version_code = _get_query_version_code()
    assert query_version_code is not None
    results = scan_api.get_scan_results_of_a_specific_query(scan_id, query_version_code)
    assert len(results) > 0


def test_get_scan_results_for_a_specific_query_group_by_best_fix_location():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    query_version_code = _get_query_version_code()
    assert query_version_code is not None
    results = scan_api.get_scan_results_for_a_specific_query_group_by_best_fix_location(scan_id, query_version_code)
    assert len(results) > 0


def test_update_scan_result_labels_fields():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    is_successful = scan_api.update_scan_result_labels_fields(
        scan_id=scan_id, result_id=1, state=1,
        severity=None, user_assignment=None,
        comment="This is a test comment",
    )
    assert is_successful is True


@pytest.mark.skip(reason="Requires a local zip file not available in CI")
def test_create_new_scan_with_settings():
    project_id = get_project_id()
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()
    preset_id = projects_api.get_preset_id_by_name("All")
    file_name = "../../JavaVulnerableLab-master.zip"
    zip_file_path = normpath(join(dirname(__file__), file_name))
    scan = scan_api.create_new_scan_with_settings(
        project_id=project_id, preset_id=preset_id,
        comment="preset All, private scan",
        zipped_source_file_path=zip_file_path,
        custom_fields={"some1": "baby2"},
        api_version="4",
    )
    assert scan is not None


def test_get_scan_result_labels_fields():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    fields = scan_api.get_scan_result_labels_fields(scan_id=scan_id, result_id=1)
    assert fields is not None


def test_get_scan_logs():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    try:
        logs = scan_api.get_scan_logs(scan_id=scan_id)
        assert logs is not None
    except ValueError:
        pytest.skip("Scan logs not available for this scan")


def _get_metrics(fn, scan_id):
    try:
        result = fn(scan_id=scan_id)
        assert result is not None
    except ValueError:
        pytest.skip("Scan metrics not available for this scan")


def test_get_basic_metrics_of_a_scan():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No qualifying finished full scan found")
    _get_metrics(ScansAPI().get_basic_metrics_of_a_scan, scan_id)


def test_get_parsed_files_metrics_of_a_scan():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No qualifying finished full scan found")
    _get_metrics(ScansAPI().get_parsed_files_metrics_of_a_scan, scan_id)


def test_get_failed_queries_metrics_of_a_scan():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No qualifying finished full scan found")
    _get_metrics(ScansAPI().get_failed_queries_metrics_of_a_scan, scan_id)


def test_get_failed_general_queries_metrics_of_a_scan():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No qualifying finished full scan found")
    _get_metrics(ScansAPI().get_failed_general_queries_metrics_of_a_scan, scan_id)


def test_get_succeeded_general_queries_metrics_of_a_scan():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No qualifying finished full scan found")
    _get_metrics(ScansAPI().get_succeeded_general_queries_metrics_of_a_scan, scan_id)


def test_get_result_path_comments_history():
    scan_id = _get_scan_id()
    result = ScansAPI().get_result_path_comments_history(scan_id=scan_id, path_id=1)
    assert result is not None


def test_lock_scan():
    scan_id = _get_scan_id()
    result = ScansAPI().lock_scan(scan_id=scan_id)
    assert result is True


def test_unlock_scan():
    scan_id = _get_scan_id()
    result = ScansAPI().unlock_scan(scan_id=scan_id)
    assert result is True


def test_get_scan_result_labels_action_fields():
    scan_id = _get_scan_id()
    result = ScansAPI().get_scan_result_labels_action_fields(scan_id=scan_id, path_id=1)
    assert result is not None


def test_get_compare_results_of_two_scans():
    scan_api = ScansAPI()
    project_id = get_project_id()
    scans = scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Finished", last=2)
    if len(scans) < 2:
        pytest.skip("Need at least 2 finished scans to compare")
    result = scan_api.get_compare_results_of_two_scans(
        old_scan_id=scans[1].id, new_scan_id=scans[0].id
    )
    assert result is not None


def test_get_compare_results_summary_of_two_scans():
    scan_api = ScansAPI()
    project_id = get_project_id()
    scans = scan_api.get_all_scans_for_project(project_id=project_id, scan_status="Finished", last=2)
    if len(scans) < 2:
        pytest.skip("Need at least 2 finished scans to compare")
    result = scan_api.get_compare_results_summary_of_two_scans(
        old_scan_id=scans[1].id, new_scan_id=scans[0].id
    )
    assert result is not None


def test_get_a_collection_of_scans_by_project():
    project_id = get_project_id()
    scan_api = ScansAPI()

    result = scan_api.get_a_collection_of_scans_by_project()
    assert result is not None
    result = scan_api.get_a_collection_of_scans_by_project(last=10)
    assert result is not None
    result = scan_api.get_a_collection_of_scans_by_project(project_id=project_id)
    assert result is not None
    try:
        scan_api.get_a_collection_of_scans_by_project(scan_status="Finished")
    except ValueError:
        pass
    result = scan_api.get_a_collection_of_scans_by_project(last=10, project_id=project_id)
    assert result is not None
    result = scan_api.get_a_collection_of_scans_by_project(last=10, project_id=project_id, scan_status="Finished")
    assert result is not None
