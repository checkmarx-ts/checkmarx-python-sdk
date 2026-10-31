import pytest
from CheckmarxPythonSDK.CxOne import (
    get_sast_aggregate_results,
    get_sast_aggregate_results_comparison,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def _get_two_sast_scan_ids_same_project():
    result = _ScansAPI().get_a_list_of_scans(limit=30, statuses=["Completed"])
    by_project = {}
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            by_project.setdefault(scan.project_id, []).append(scan.id)
    for scan_ids in by_project.values():
        if len(scan_ids) >= 2:
            return scan_ids[0], scan_ids[1]
    return None, None


def test_get_sast_aggregate_results():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    response = get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=["QUERY"],
    )
    assert response is not None
    assert "summaries" in response
    assert "totalCount" in response


def test_get_sast_aggregate_results_comparison():
    scan_id, base_scan_id = _get_two_sast_scan_ids_same_project()
    if not scan_id:
        pytest.skip("No project with 2+ completed SAST scans found")
    response = get_sast_aggregate_results_comparison(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        group_by_field=["QUERY"],
    )
    assert response is not None
    assert "summaries" in response
    assert "totalCount" in response


def test_get_sast_aggregate_results_comparison_cwe_group_by_and_new_filters():
    # CWE was missing from group_by_field's documented allowed values
    # before this was fixed; evaluation_status/correlation_id are new
    scan_id, base_scan_id = _get_two_sast_scan_ids_same_project()
    if not scan_id:
        pytest.skip("No project with 2+ completed SAST scans found")
    response = get_sast_aggregate_results_comparison(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        group_by_field=["CWE"],
        evaluation_status=True,
        correlation_id="11111111-1111-1111-1111-111111111111",
    )
    assert response is not None
    assert "summaries" in response


def test_get_sast_aggregate_results_comparison_is_ai_generated_server_bug():
    # KNOWN LIVE SERVER BUG: is_ai_generated=0 500s server-side
    # ("unknown filter operation 9"); value 1 works fine. Documents
    # the bug rather than silently tolerating a regression either way
    # -- if Checkmarx fixes this, this test starts failing on the
    # pytest.raises and should be updated to assert success instead.
    scan_id, base_scan_id = _get_two_sast_scan_ids_same_project()
    if not scan_id:
        pytest.skip("No project with 2+ completed SAST scans found")

    response = get_sast_aggregate_results_comparison(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        group_by_field=["CWE"],
        is_ai_generated=1,
    )
    assert response is not None

    with pytest.raises(ValueError, match="unknown filter operation"):
        get_sast_aggregate_results_comparison(
            scan_id=scan_id,
            base_scan_id=base_scan_id,
            group_by_field=["CWE"],
            is_ai_generated=0,
        )


def test_get_sast_aggregate_results_state_and_cwe_group_by():
    # STATE/CWE were missing from group_by_field's documented allowed
    # values before this was fixed
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    response = get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=["STATE", "CWE"],
    )
    assert response is not None
    assert "summaries" in response


def test_get_sast_aggregate_results_with_new_filters():
    # exercises filters added when this method was expanded to full
    # doc parity (previously only ~12 of ~38 query params existed)
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    response = get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=["QUERY"],
        severity=["HIGH", "MEDIUM"],
        cwe_id=79,
        cwe_id_operation="EQUAL",
        search="main",
        confidence_score=50,
        confidence_score_operation="GREATER_THAN",
        is_ai_generated=0,
        is_ai_generated_operation="EQUAL",
        result_ids=["nonexistent-hash"],
        correlation_id="11111111-1111-1111-1111-111111111111",
    )
    assert response is not None
    assert "summaries" in response
