"""
    tests.test_projects_api

    :copyright Checkmarx
    :license GPL-3

"""
import time
from os.path import normpath, join, dirname
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI

from .. import get_project_id


def test_create_new_scan():
    project_id = get_project_id()
    scan_api = ScansAPI()
    # create new scan without scan custom fields
    scan_api.create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True,
                             comment="scan from REST API")
    time.sleep(30)
    # create new scan without scan custom fields
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


def test_get_last_scan_id_of_a_project():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True, only_completed_scans=True,
                                                     only_real_scans=True, only_full_scans=True)
    assert scan_id > 1


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
    result = scan_api.add_or_update_a_comment_by_scan_id(scan_id, "updated scan comment")
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


"""
def test_assign_ticket_to_scan_results():
    scan_api = ScansAPI()
    results_id = "1000004-5"
    ticket_id = "10060"
    # is_successful = scan_api.assign_ticket_to_scan_results(results_id, ticket_id)
    # assert is_successful is True
"""


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


def get_similarity_ids_of_a_scan(scan_id):
    from CheckmarxPythonSDK.CxODataApiSDK.HttpRequests import get_request
    url = f"/Cxwebinterface/odata/v1/Scans({scan_id})/Results?$select=SimilarityId,PathId"
    return get_request(relative_url=url)


def update_csv_report(cx_report_file_path, scan_id):
    """
    update CSV report by add the similarityID column (data retrieved by using ODATA API)
    Args:
        cx_report_file_path:
        scan_id:

    Returns:

    """
    import pathlib
    if not pathlib.Path(cx_report_file_path).exists():
        return
    import csv
    from collections import OrderedDict
    similarity_id_path_ids = get_similarity_ids_of_a_scan(scan_id=scan_id)
    sim_path_dict = {}
    for pair in similarity_id_path_ids:
        sim_path_dict[pair.get("PathId")] = pair.get("SimilarityId")
    csv_content = []
    with open(cx_report_file_path, newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        field_names = reader.fieldnames
        field_names = [item for item in field_names]
        field_names.append('SimilarityID')
        for row in reader:
            path_id = row.get("Link").split('&')[2].split('=')[1]
            path_id = int(path_id)
            similarity_id = sim_path_dict.get(path_id)
            new_ordered_dict = OrderedDict()
            for key, value in row.items():
                new_ordered_dict[key] = value
            new_ordered_dict['SimilarityID'] = similarity_id
            csv_content.append(new_ordered_dict)
    with open(cx_report_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='unix')
        writer.writeheader()
        writer.writerows(csv_content)


def test_register_scan_report():
    project_id = get_project_id()

    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True, only_completed_scans=False,
                                                     only_real_scans=False, only_full_scans=False,
                                                     only_public_scans=False)

    report_type = "CSV"
    scan_report = scan_api.register_scan_report(scan_id, report_type)
    assert scan_report is not None

    report_id = scan_report.report_id
    report_status = scan_api.get_report_status_by_id(report_id)
    assert report_status is not None
    time.sleep(30)
    report_content = scan_api.get_report_by_id(report_id)
    assert report_content is not None
    with open(str("cx-report.csv"), "wb") as f_out:
        f_out.write(report_content)

    update_csv_report(r"C:\Users\HappyY\Documents\SourceCode\GitHub\checkmarx-python-sdk\tests\cx-report.csv", scan_id)
query_version_code = 56142311


def test_get_scan_results_of_a_specific_query():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    results = scan_api.get_scan_results_of_a_specific_query(scan_id, query_version_code)
    assert len(results) > 0


def test_get_scan_results_for_a_specific_query_group_by_best_fix_location():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    results = scan_api.get_scan_results_for_a_specific_query_group_by_best_fix_location(scan_id, query_version_code)
    assert len(results) > 0


def test_update_scan_result_labels_fields():
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    is_successful = scan_api.update_scan_result_labels_fields(scan_id=scan_id,
                                                              result_id=1,
                                                              state=1,
                                                              severity=None,
                                                              user_assignment=None,
                                                              comment="This is a test comment")
    assert is_successful is True


def test_create_new_scan_with_settings():
    project_id = get_project_id()
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()
    preset_id = projects_api.get_preset_id_by_name("All")
    file_name = "../../JavaVulnerableLab-master.zip"
    zip_file_path = normpath(join(dirname(__file__), file_name))
    scan = scan_api.create_new_scan_with_settings(project_id=project_id, preset_id=preset_id,
                                                  comment="prest All, private scan",
                                                  zipped_source_file_path=zip_file_path,
                                                  custom_fields={"some1": "baby2"},
                                                  api_version="1.2")
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

    logs = scan_api.get_scan_logs(scan_id=scan_id)

    assert logs is not None


def test_get_basic_metrics_of_a_scan():
    """
    Could be 404 Not Found
    Returns:

    """
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)
    statistics = scan_api.get_basic_metrics_of_a_scan(scan_id=scan_id)
    assert statistics is not None


def test_get_parsed_files_metrics_of_a_scan():
    """
    Could be 404 Not Found
    Returns:

    """
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    parsed_files = scan_api.get_parsed_files_metrics_of_a_scan(scan_id=scan_id)
    assert parsed_files is not None


def test_get_failed_queries_metrics_of_a_scan():
    """
    Could be 404 Not Found
    Returns:

    """
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    failed_queries = scan_api.get_failed_queries_metrics_of_a_scan(scan_id=scan_id)
    assert failed_queries is not None


def test_get_failed_general_queries_metrics_of_a_scan():
    """
    Could be 404 Not Found
    Returns:

    """
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    failed_general_queries = scan_api.get_failed_general_queries_metrics_of_a_scan(scan_id=scan_id)
    assert failed_general_queries is not None


def test_get_succeeded_general_queries_metrics_of_a_scan():
    """
    Could be 404 Not Found
    Returns:

    """
    project_id = get_project_id()
    scan_api = ScansAPI()
    scan_id = scan_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)

    succeeded_general_queries = scan_api.get_succeeded_general_queries_metrics_of_a_scan(scan_id=scan_id)
    assert succeeded_general_queries is not None
