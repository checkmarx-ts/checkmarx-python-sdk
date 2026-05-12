import pytest
from typing import List
from CheckmarxPythonSDK.CxOne import (
    get_all_predicates_for_similarity_id,
    get_latest_predicates_for_similarity_id,
    predicate_severity_and_state_by_similarity_id_and_project_id,
    update_predicate_comment_by_predicate_id,
    recalculate_summary_counters,
    delete_a_predicate_history,
)

from CheckmarxPythonSDK.CxOne.dto import (
    PredicateHistory,
    Predicate,
    PredicateWithCommentJSON,
    PredicateWithCommentsJSON,
    CommentJSON,
    WebError
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI


def _get_sast_scan_and_project_id():
    """Return (scan_id, project_id) for a completed SAST scan, or (None, None)."""
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id, scan.project_id
    return None, None


def test_get_all_predicates_for_similarity_id():
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id: str = "491614176"
    project_ids: List[str] = [project_id]
    include_comment_json: bool = True
    result = get_all_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        include_comment_json=include_comment_json,
        scan_id=scan_id,
    )
    assert result is not None


def test_get_latest_predicates_for_similarity_id():
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id: str = "491614176"
    project_ids: List[str] = [project_id]
    result = get_latest_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        scan_id=scan_id,
    )
    assert result is not None


def test_predicate_severity_and_state_by_similarity_id_and_project_id():
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    request_body: List[dict] = [{"similarityId": "491614176", "projectId": project_id,
                                 "scanId": scan_id, "severity": "HIGH",
                                 "state": "CONFIRMED", "comment": "test"}]
    result = predicate_severity_and_state_by_similarity_id_and_project_id(data=request_body)
    assert result is not None


@pytest.mark.skip(reason="410 - endpoint not supported in current API version")
def test_update_predicate_comment_by_predicate_id():
    request_body: List[dict] = [
        {
            "similarityId": "491614176",
            "predicateId": "1d5c3829-18b4-45c6-b52a-f0646bb8fdf1",
            "projectId": "c1ae5825-486a-43a5-b454-67fefd1f2545",
            "comment": "update predicate comment"
        }
    ]
    result = update_predicate_comment_by_predicate_id(data=request_body)
    assert result is not None


@pytest.mark.skip(reason="400 - recalculate endpoint requires predicates-enabled project that does not exist in this tenant")
def test_recalculate_summary_counters():
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    request_body: dict = {
        "projectId": project_id,
        "scanId": scan_id
    }
    result = recalculate_summary_counters(data=request_body)
    assert result is True


@pytest.mark.skip(reason="410 - endpoint not supported in current API version")
def test_delete_a_predicate_history():
    similarity_id: str = "491614176"
    project_id: str = "c1ae5825-486a-43a5-b454-67fefd1f2545"
    predicate_id: str = "1d5c3829-18b4-45c6-b52a-f0646bb8fdf1"
    result = delete_a_predicate_history(
        similarity_id=similarity_id,
        project_id=project_id,
        predicate_id=predicate_id
    )
    assert result is not None
