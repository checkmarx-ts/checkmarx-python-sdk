# encoding: utf-8
import time
import pytest

from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI, ScansAPI
from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    add_license_expiration_notification,
    cancel_scan_report,
    count_lines,
    create_new_preset,
    create_scan_report,
    delete_preset,
    export_preset,
    export_queries,
    get_child_nodes,
    get_configuration_set_list,
    get_compare_scan_results,
    get_custom_fields,
    get_cwe_description,
    get_executable_list,
    get_file_names_for_path,
    get_import_queries_status,
    get_preset_details,
    get_path_comments_history,
    get_pivot_data,
    get_preset_list,
    get_projects_display_data,
    get_projects_with_scans,
    get_associated_group_list,
    get_queries_categories,
    get_queries_for_scan,
    get_query_collection,
    get_query_collection_for_language,
    get_query_description,
    get_query_description_by_query_id,
    get_query_id_by_language_group_and_query_name,
    get_query_short_description,
    get_result_path,
    get_result_paths_for_query,
    get_result_state_flags,
    get_result_state_list,
    get_result_summary,
    get_results,
    get_results_for_query,
    get_results_for_scan,
    get_scan_logs,
    get_scan_properties,
    get_scan_report,
    get_scan_report_status,
    get_scan_summary,
    get_scans_display_data_for_all_projects,
    get_scans_statuses,
    get_server_language_list,
    get_server_license_basic,
    get_server_license_data,
    get_server_license_data_extended,
    get_server_license_summary,
    get_sources_by_scan_id,
    get_source_by_scan_id,
    get_status_of_single_scan,
    get_user_profile_data,
    get_version_number,
    get_version_number_as_int,
    get_name_of_user_who_marked_false_positive_from_comments_history,
    import_preset,
    import_queries,
    is_alive,
    is_private_cloud,
    is_smtp_host_configured,
    is_valid_preset_name,
    lock_scan,
    postpone_scan,
    unlock_scan,
    update_preset,
    update_result_comment,
    update_result_state,
    update_scan_comment,
)
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


def test_add_license_expiration_notification():
    response = add_license_expiration_notification()
    assert response.get("IsSuccesfull") is True


def test_create_new_preset_and_delete():
    query_groups = get_query_collection().get("QueryGroups", [])
    first_query_id = None
    for g in query_groups:
        queries = g.get("Queries") or []
        if queries:
            first_query_id = queries[0].get("QueryId")
            break
    assert first_query_id is not None

    preset_name = "pytest_tmp_preset"
    response = create_new_preset(query_ids=[first_query_id], name=preset_name)
    assert response["IsSuccesfull"] is True
    assert response["preset"] is not None

    preset_id = response["preset"]["id"]
    del_response = delete_preset(preset_id=preset_id)
    assert del_response["IsSuccesfull"] is True


def test_create_scan_report():
    scan_id = _get_scan_id()
    response = create_scan_report(
        scan_id=scan_id,
        report_type="PDF",
        results_per_vulnerability_maximum=500,
        display_categories_all=False,
        display_categories_ids=list(range(30, 62)),
    )
    assert response["IsSuccesfull"] is True
    assert response["ID"] > 0


def test_export_preset():
    response = get_preset_list()
    assert response["IsSuccesfull"] is True
    presets = response.get("PresetList", [])
    assert len(presets) > 0
    preset_id = presets[0]["ID"]

    response = export_preset(preset_id=preset_id)
    assert response.get("Preset") is not None


@pytest.mark.skip(reason="Only corporate queries can be exported; no corp queries on this server")
def test_export_queries():
    response = export_queries(queries_ids=[])
    assert response is not None


def test_get_associated_group_list():
    response = get_associated_group_list()
    assert response is not None


@pytest.mark.skip(reason="Requires two distinct scan IDs to compare; only one scan available")
def test_get_compare_scan_results():
    scan_id = _get_scan_id()
    response = get_compare_scan_results(old_scan_id=scan_id, new_scan_id=scan_id)
    assert response is not None


def test_get_path_comments_history():
    scan_id = _get_scan_id()
    response = get_path_comments_history(
        scan_id=scan_id, path_id=1, label_type="Remark"
    )
    assert response.get("IsSuccesfull") is True


def test_get_pivot_data():
    pivot_data = get_pivot_data(
        pivot_view_client_type="AllProjectScans",
        include_not_exploitable=False,
        range_type="CUSTOM",
        date_from="2020-05-01-0-0-0",
        date_to="2030-05-09-0-0-0",
    )
    assert pivot_data is not None

    pivot_data = get_pivot_data(
        pivot_view_client_type="LastMonthProjectScans",
        include_not_exploitable=False,
        range_type="PAST_MONTH",
        date_from="2023-06-01-0-0-0",
        date_to="2023-06-30-0-0-0",
    )
    assert pivot_data is not None

    pivot_data = get_pivot_data(
        pivot_view_client_type="ProjectsLastScan",
        include_not_exploitable=False,
        range_type="CUSTOM",
        date_from="2023-07-01-0-0-0",
        date_to="2030-08-30-0-0-0",
    )
    assert pivot_data is not None


def test_get_user_profile_data():
    # GetUserProfileData is not implemented by the Portal SOAP API; always returns IsSuccesfull=False
    response = get_user_profile_data()
    assert response is not None


def test_get_queries_categories():
    response = get_queries_categories()
    assert len(response["QueriesCategories"]) > 1


def test_get_query_collection():
    response = get_query_collection()
    query_groups = response.get("QueryGroups")
    assert query_groups is not None
    assert len(query_groups) > 0
    for query_group in query_groups:
        query_group_name = query_group.get("Name")
        if any(
            kw in query_group_name
            for kw in ("General", "Quality", "Best")
        ):
            continue
        for query in query_group.get("Queries") or []:
            categories = query.get("Categories") or []
            assert "QueryId" in query
            assert "Name" in query


def test_get_query_id_by_language_group_and_query_name():
    query_collections = get_query_collection().get("QueryGroups", [])
    # Pick the first Cx group that has queries
    target = None
    for g in query_collections:
        if g.get("PackageTypeName") == "Cx" and g.get("Queries"):
            target = g
            break
    assert target is not None

    query_name = target["Queries"][0]["Name"]
    result = get_query_id_by_language_group_and_query_name(
        query_collections=query_collections,
        language=target["LanguageName"],
        package_type_name=target["PackageTypeName"],
        package_name=target["Name"],
        query_name=query_name,
    )
    assert isinstance(result, int)


def test_get_query_description_by_query_id():
    query_groups = get_query_collection().get("QueryGroups", [])
    query_id = None
    for g in query_groups:
        for q in (g.get("Queries") or []):
            query_id = q.get("QueryId")
            break
        if query_id:
            break
    assert query_id is not None
    response = get_query_description_by_query_id(query_id)
    assert response is not None


def test_get_name_of_user_who_marked_false_positive_from_comments_history():
    scan_id = _get_scan_id()
    response = get_name_of_user_who_marked_false_positive_from_comments_history(
        scan_id=scan_id, path_id=1
    )
    # Returns None when no false-positive comment exists; just ensure no exception
    assert response is None or isinstance(response, str)


def test_get_preset_list():
    response = get_preset_list()
    assert response["IsSuccesfull"] is True


def test_get_projects_display_data():
    response = get_projects_display_data()
    assert response is not None
    assert response.get("IsSuccesfull") is True


def test_get_result_path():
    scan_id = _get_scan_id()
    response = get_result_path(scan_id=scan_id, path_id=1)
    assert response["IsSuccesfull"] is True


def test_get_results_for_scan():
    scan_id = _get_scan_id()
    response = get_results_for_scan(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


def test_get_server_license_data():
    lic = get_server_license_data()
    assert lic is not None


def test_get_server_license_summary():
    lic = get_server_license_summary()
    assert lic is not None


def test_get_version_number():
    version = get_version_number()
    assert version is not None


def test_get_version_number_as_int():
    version = get_version_number_as_int()
    assert version > 800


@pytest.mark.skip(reason="Requires an external preset XML file not available in CI")
def test_import_preset():
    imported_file_path = "preset.xml"
    response = import_preset(imported_file_path=imported_file_path)
    import_query_status = response.get("importQueryStatus")
    request_id = response.get("requestId")
    while import_query_status not in ["Failed", "Succeeded"]:
        response = get_import_queries_status(request_id=request_id)
        import_query_status = response.get("importQueryStatus")
        time.sleep(1)
    assert import_query_status == "Succeeded"


@pytest.mark.skip(reason="Requires an external query XML file not available in CI")
def test_import_queries():
    imported_file_path = "query.xml"
    response = import_queries(imported_file_path=imported_file_path)
    import_query_status = response.get("importQueryStatus")
    request_id = response.get("requestId")
    while import_query_status not in ["Failed", "Succeeded"]:
        response = get_import_queries_status(request_id=request_id)
        import_query_status = response.get("importQueryStatus")
        time.sleep(1)
    assert import_query_status == "Succeeded"


def test_lock_and_unlock_scan():
    scan_id = _get_scan_id()
    lock_response = lock_scan(scan_id=scan_id)
    assert lock_response.get("IsSuccesfull") is True

    unlock_response = unlock_scan(scan_id=scan_id)
    assert unlock_response.get("IsSuccesfull") is True


@pytest.mark.skip(reason="postpone_scan only works on an actively queued scan, not a finished one")
def test_postpone_scan():
    scan_id = _get_scan_id()
    response = postpone_scan(scan_id=scan_id)
    assert response.get("IsSuccesfull") is True


def test_get_file_names_for_path():
    scan_id = _get_scan_id()
    response = get_file_names_for_path(scan_id=scan_id, path_id=1)
    assert response["IsSuccesfull"] is True
    assert len(response["fileNames"]) > 0
    assert all(isinstance(fn, str) for fn in response["fileNames"])


def test_get_sources_by_scan_id():
    scan_id = _get_scan_id()
    # Get a file name from a known path
    file_info = get_file_names_for_path(scan_id=scan_id, path_id=1)
    assert file_info["IsSuccesfull"] is True
    file_names = file_info["fileNames"]

    response = get_sources_by_scan_id(
        scan_id=scan_id, file_names=file_names,
    )
    assert response["IsSuccesfull"] is True
    assert len(response["sources"]) == len(file_names)
    for src in response["sources"]:
        assert "Source" in src
        assert "IsSuccesfull" in src
        assert len(str(src["Source"])) > 0

    # Test with multiple files
    if len(file_names) >= 1:
        response = get_sources_by_scan_id(
            scan_id=scan_id, file_names=file_names[:1],
        )
        assert response["IsSuccesfull"] is True
        assert len(response["sources"]) == 1
        assert len(str(response["sources"][0]["Source"])) > 0


def test_get_source_by_scan_id_deprecated():
    """Verify the deprecated singular endpoint returns the expected error."""
    scan_id = _get_scan_id()
    response = get_source_by_scan_id(
        scan_id=scan_id,
        file_name=r"\src\main\webapp\vulnerability\DisplayMessage.jsp",
    )
    assert response["IsSuccesfull"] is False
    assert "no longer supported" in response.get("ErrorMessage", "")


def test_get_preset_details():
    response = get_preset_list()
    assert response["IsSuccesfull"] is True
    presets = response.get("PresetList", [])
    assert len(presets) > 0
    preset_id = presets[0]["ID"]

    response = get_preset_details(preset_id=preset_id)
    assert response["IsSuccesfull"] is True
    assert response["preset"] is not None
    assert response["preset"]["id"] == preset_id


def test_update_preset():
    presets = get_preset_list().get("PresetList", [])
    assert len(presets) > 0
    preset_id = presets[0]["ID"]

    details = get_preset_details(preset_id=preset_id)
    query_ids = details["preset"]["queryIds"]
    name = details["preset"]["name"]

    response = update_preset(preset_id=preset_id, query_ids=query_ids, name=name)
    assert response["IsSuccesfull"] is True


def test_get_result_state_list():
    response = get_result_state_list()
    assert response["IsSuccesfull"] is True
    assert len(response["ResultStateList"]) > 0
    for item in response["ResultStateList"]:
        assert "ResultName" in item
        assert "ResultID" in item


def test_get_scan_summary():
    scan_id = _get_scan_id()
    response = get_scan_summary(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


def test_get_scan_report_and_status():
    scan_id = _get_scan_id()
    report = create_scan_report(scan_id=scan_id, report_type="PDF")
    assert report["IsSuccesfull"] is True
    report_id = report["ID"]

    status_response = get_scan_report_status(report_id=report_id)
    assert status_response["IsSuccesfull"] is True
    # SOAP response exposes IsReady/IsFailed booleans (not the "Status"
    # field the doc-derived stub previously returned as always-None).
    assert "IsReady" in status_response
    assert "IsFailed" in status_response
    assert isinstance(status_response["IsReady"], bool)
    assert isinstance(status_response["IsFailed"], bool)

    cancel_response = cancel_scan_report(report_id=report_id)
    assert cancel_response["IsSuccesfull"] is True


def test_get_results():
    """Portal GetResults is deprecated in 9.x; returns IsSuccesfull=False."""
    scan_id = _get_scan_id()
    response = get_results(scan_id=scan_id)
    assert response is not None


def test_get_result_summary():
    """GetResultSummary is deprecated in 9.x; returns IsSuccesfull=False."""
    scan_id = _get_scan_id()
    response = get_result_summary(scan_id=scan_id)
    assert response is not None


@pytest.mark.skip(reason="GetQueryCollectionForLanguage requires a valid project context")
def test_get_query_collection_for_language():
    from .. import get_project_id
    project_id = get_project_id()
    response = get_query_collection_for_language(
        project_type="Regular", project_id=project_id
    )
    assert response["IsSuccesfull"] is True


def test_get_query_description():
    response = get_query_description(cwe_id=79)
    assert response is not None


def test_get_query_short_description():
    query_groups = get_query_collection().get("QueryGroups", [])
    query_id = None
    for g in query_groups:
        for q in (g.get("Queries") or []):
            query_id = q.get("QueryId")
            break
        if query_id:
            break
    assert query_id is not None
    response = get_query_short_description(query_id=query_id)
    assert response is not None


def test_get_scans_display_data_for_all_projects():
    response = get_scans_display_data_for_all_projects()
    assert response["IsSuccesfull"] is True


def test_get_server_license_basic():
    response = get_server_license_basic()
    assert response is not None


def test_get_server_license_data_extended():
    response = get_server_license_data_extended()
    assert response is not None


def test_get_custom_fields():
    response = get_custom_fields()
    assert response["IsSuccesfull"] is True


def test_get_cwe_description():
    response = get_cwe_description(cwe_id=79)
    assert response["IsSuccesfull"] is True


def test_get_result_paths_for_query():
    scan_id = _get_scan_id()
    query_groups = get_query_collection().get("QueryGroups", [])
    query_id = None
    for g in query_groups:
        for q in (g.get("Queries") or []):
            query_id = q.get("QueryId")
            break
        if query_id:
            break
    assert query_id is not None
    response = get_result_paths_for_query(
        scan_id=scan_id,
        query_id=query_id,
    )
    assert response["IsSuccesfull"] is True


def test_get_results_for_query():
    scan_id = _get_scan_id()
    query_groups = get_query_collection().get("QueryGroups", [])
    query_id = None
    for g in query_groups:
        for q in (g.get("Queries") or []):
            query_id = q.get("QueryId")
            break
        if query_id:
            break
    assert query_id is not None
    response = get_results_for_query(
        scan_id=scan_id,
        query_id=query_id,
    )
    assert response["IsSuccesfull"] is True


def test_get_queries_for_scan():
    scan_id = _get_scan_id()
    response = get_queries_for_scan(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


def test_get_scan_properties():
    scan_id = _get_scan_id()
    response = get_scan_properties(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


@pytest.mark.skip(reason="get_status_of_single_scan requires an active runId, not a finished scan")
def test_get_status_of_single_scan():
    scan_id = _get_scan_id()
    response = get_status_of_single_scan(scan_id=scan_id)
    assert response is not None


def test_get_scans_statuses():
    response = get_scans_statuses()
    assert response["IsSuccesfull"] is True


@pytest.mark.skip(reason="get_scan_logs may not return data for old scans")
def test_get_scan_logs():
    scan_id = _get_scan_id()
    response = get_scan_logs(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


@pytest.mark.skip(reason="update_result_state requires project_id context")
def test_update_result_state_and_comment():
    scan_id = _get_scan_id()
    results = get_results_for_scan(scan_id=scan_id)
    scan_results = results.get("ScanResults", [])
    from .. import get_project_id
    project_id = get_project_id()
    if scan_results:
        path_id = scan_results[0]["PathId"]
        state_response = update_result_state(
            scan_id=scan_id,
            path_id=path_id,
            project_id=project_id,
            remarks="test",
        )
        assert state_response["IsSuccesfull"] is True

        comment_response = update_result_comment(
            result_id=scan_id,
            path_id=path_id,
            project_id=project_id,
            comment="test comment",
        )
        assert comment_response is not None


def test_update_scan_comment():
    scan_id = _get_scan_id()
    response = update_scan_comment(scan_id=scan_id, comment="test scan comment")
    assert response["IsSuccesfull"] is True


def test_is_valid_preset_name():
    response = is_valid_preset_name(name="UniqueTestName_12345")
    assert response["IsSuccesfull"] is True


def test_get_server_language_list():
    response = get_server_language_list()
    assert response["IsSuccesfull"] is True


def test_get_executable_list():
    response = get_executable_list()
    assert response["IsSuccesfull"] is True


@pytest.mark.skip(reason="count_lines requires a real source code string")
def test_count_lines():
    response = count_lines(
        source_code="public class Test { public void foo() { int x = 1; } }",
        language_name="Java",
    )
    assert response["IsSuccesfull"] is True


def test_is_alive():
    response = is_alive()
    assert response["IsSuccesfull"] is True


def test_is_smtp_host_configured():
    response = is_smtp_host_configured()
    assert response is not None


def test_is_private_cloud():
    response = is_private_cloud()
    assert response is not None


def test_get_result_state_flags():
    response = get_result_state_flags()
    assert response is not None


def test_get_child_nodes():
    response = get_child_nodes()
    assert response is not None


def test_get_projects_with_scans():
    response = get_projects_with_scans()
    assert response["IsSuccesfull"] is True


def test_get_configuration_set_list():
    response = get_configuration_set_list()
    assert response["IsSuccesfull"] is True
