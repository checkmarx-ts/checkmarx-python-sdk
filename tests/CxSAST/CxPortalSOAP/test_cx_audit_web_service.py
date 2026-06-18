import pytest
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    get_files_extensions,
    get_source_code_for_scan,
    upload_queries,
    audit_get_results as get_results,
    audit_get_result_summary as get_result_summary,
    audit_get_result_state_list as get_result_state_list,
    get_project_scans,
    audit_get_projects_with_scans as get_projects_with_scans,
    audit_get_query_collection as get_query_collection,
    audit_get_query_collection_for_language as get_query_collection_for_language,
    audit_get_query_description as get_query_description,
    audit_get_query_description_by_query_id as get_query_description_by_query_id,
    audit_get_queries_categories as get_queries_categories,
    audit_get_preset_details as get_preset_details,
    audit_get_preset_list as get_preset_list,
    audit_get_path_comments_history as get_path_comments_history,
    get_project_configuration,
    get_license_details,
    get_engine_configuration,
    get_hierarchy_group_tree,
    get_ancestry_group_tree,
    keep_alive,
    get_cache,
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


def test_get_files_extensions():
    response = get_files_extensions()
    assert response is not None


def test_get_source_code_for_scan():
    scan_id = _get_scan_id()
    response = get_source_code_for_scan(scan_id=scan_id)
    assert response is not None


@pytest.mark.skip(reason="upload_queries requires a query groups dict structure")
def test_upload_queries():
    response = upload_queries(query_groups=[])
    assert response is not None


def test_get_results():
    scan_id = _get_scan_id()
    response = get_results(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


def test_get_result_summary():
    scan_id = _get_scan_id()
    response = get_result_summary(scan_id=scan_id)
    assert response["IsSuccesfull"] is True


def test_get_result_state_list():
    response = get_result_state_list()
    assert response["IsSuccesfull"] is True
    assert len(response["ResultStateList"]) > 0


def test_get_project_scans():
    project_id = get_project_id()
    response = get_project_scans(project_id=project_id)
    assert response["IsSuccesfull"] is True


def test_get_projects_with_scans():
    response = get_projects_with_scans()
    assert response["IsSuccesfull"] is True


def test_get_query_collection():
    response = get_query_collection()
    assert response["IsSuccesfull"] is True
    assert len(response["QueryGroups"]) > 0


@pytest.mark.skip(reason="GetQueryCollectionForLanguage requires a valid project context")
def test_get_query_collection_for_language():
    response = get_query_collection_for_language(
        project_type="Regular", project_id=0
    )
    assert response["IsSuccesfull"] is True


def test_get_query_description():
    response = get_query_description(cwe_id=79)
    assert response is not None


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
    response = get_query_description_by_query_id(query_id=query_id)
    assert response is not None


def test_get_queries_categories():
    response = get_queries_categories()
    assert response is not None


def test_get_preset_details():
    response = get_preset_list()
    assert response["IsSuccesfull"] is True
    presets = response.get("PresetList", [])
    if presets:
        preset_id = presets[0]["ID"]
        response = get_preset_details(preset_id=preset_id)
        assert response["IsSuccesfull"] is True
        assert response["preset"] is not None


def test_get_preset_list():
    response = get_preset_list()
    assert response["IsSuccesfull"] is True


def test_get_path_comments_history():
    scan_id = _get_scan_id()
    response = get_path_comments_history(
        scan_id=scan_id, path_id=1, label_type="Remark"
    )
    assert response.get("IsSuccesfull") is True


def test_get_project_configuration():
    project_id = get_project_id()
    response = get_project_configuration(project_id=project_id)
    assert response["IsSuccesfull"] is True


def test_get_license_details():
    response = get_license_details()
    assert response["IsSuccesfull"] is True


def test_get_engine_configuration():
    response = get_engine_configuration()
    assert response["IsSuccesfull"] is True


def test_get_hierarchy_group_tree():
    response = get_hierarchy_group_tree()
    assert response["IsSuccesfull"] is True


def test_get_ancestry_group_tree():
    response = get_ancestry_group_tree()
    assert response["IsSuccesfull"] is True


def test_keep_alive():
    response = keep_alive()
    assert response is not None


@pytest.mark.skip(reason="get_cache requires a valid scan_id; use 0 for basic test")
def test_get_cache():
    response = get_cache(scan_id=0)
    assert response["IsSuccesfull"] is True
