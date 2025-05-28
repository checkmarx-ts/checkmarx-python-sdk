from typing import List
from CheckmarxPythonSDK.CxOne import (
    get_all_predicates_for_similarity_id,
    get_latest_predicates_for_similarity_id,
    predicate_severity_and_state_by_similarity_id_and_project_id,
    update_predicate_comment_by_predicate_id,
    recalculate_summary_counters,
    delete_a_predicate_history
)

from CheckmarxPythonSDK.CxOne.dto import (
    PredicateHistory,
    Predicate,
    PredicateWithCommentJSON,
    PredicateWithCommentsJSON,
    CommentJSON,
    WebError
)


def test_get_all_predicates_for_similarity_id():
    similarity_id: str = "491614176"
    project_ids: List[str] = ["c1ae5825-486a-43a5-b454-67fefd1f2545"]
    include_comment_json: bool = True
    scan_id: str = "8eb0b33d-ccf0-44dc-897b-46867d130a40"
    result = get_all_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        include_comment_json=include_comment_json,
        scan_id=scan_id,
    )
    assert result is not None


def test_get_latest_predicates_for_similarity_id():
    similarity_id: str = "491614176"
    project_ids: List[str] = ["c1ae5825-486a-43a5-b454-67fefd1f2545"]
    scan_id: str = "8eb0b33d-ccf0-44dc-897b-46867d130a40"
    result = get_latest_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        scan_id=scan_id,
    )
    assert result is not None


def test_predicate_severity_and_state_by_similarity_id_and_project_id():
    request_body: List[dict] = [{"similarityId": "491614176", "projectId": "c1ae5825-486a-43a5-b454-67fefd1f2545",
                                 "scanId": "8eb0b33d-ccf0-44dc-897b-46867d130a40", "severity": "HIGH",
                                 "state": "CONFIRMED", "comment": "test"}]
    result = predicate_severity_and_state_by_similarity_id_and_project_id(request_body=request_body)
    assert result is not None


def test_update_predicate_comment_by_predicate_id():
    request_body: List[dict] = [
        {
            "similarityId": "491614176",
            "predicateId": "1d5c3829-18b4-45c6-b52a-f0646bb8fdf1",
            "projectId": "c1ae5825-486a-43a5-b454-67fefd1f2545",
            "comment": "update predicate comment"
        }
    ]
    result = update_predicate_comment_by_predicate_id(request_body=request_body)
    assert result is not None


def test_recalculate_summary_counters():
    request_body: dict = {
        "projectId": "c1ae5825-486a-43a5-b454-67fefd1f2545",
        "scanId": "8eb0b33d-ccf0-44dc-897b-46867d130a40"
    }
    result = recalculate_summary_counters(request_body=request_body)
    assert result is True


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
