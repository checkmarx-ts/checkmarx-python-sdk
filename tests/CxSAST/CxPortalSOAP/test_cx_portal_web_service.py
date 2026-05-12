# encoding: utf-8
import time
import pytest

from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI, ScansAPI
from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    add_license_expiration_notification,
    create_new_preset,
    create_scan_report,
    delete_preset,
    export_preset,
    export_queries,
    get_compare_scan_results,
    get_import_queries_status,
    get_query_collection,
    get_query_id_by_language_group_and_query_name,
    get_query_description_by_query_id,
    get_preset_list,
    get_projects_display_data,
    get_associated_group_list,
    get_server_license_data,
    get_server_license_summary,
    get_version_number,
    get_version_number_as_int,
    get_path_comments_history,
    get_user_profile_data,
    get_queries_categories,
    get_name_of_user_who_marked_false_positive_from_comments_history,
    import_preset,
    import_queries,
    lock_scan,
    postpone_scan,
    unlock_scan,
    get_results_for_scan,
    get_result_path,
    get_pivot_data,
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
