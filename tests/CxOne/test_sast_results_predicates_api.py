
from CheckmarxPythonSDK.CxOne import (
    get_all_predicates_for_similarity_id,
    get_latest_predicates_for_similarity_id,
    predicate_severity_and_state_by_similiarty_id_and_project_id,
    update_predicate_comment_by_predicate_id,
    recalculate_summary_counters,
    delete_a_predicate_history
)

from CheckmarxPythonSDK.CxOne.dto import (
    StateEnum,
    SeverityEnum,
    PredicateHistory,
    Predicate,
    PredicateWithCommentJSON,
    PredicateWitCommentsJSON,
    CommentJSON,
    WebError
)


def test_get_all_predicates_for_similarity_id():
    result = get_all_predicates_for_similarity_id(auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None, similarity_id: str, project_ids: List[str] = None, include_comment_json: bool = None, scan_id: str = None)
    assert result is not None


def test_get_latest_predicates_for_similarity_id():
    result = get_latest_predicates_for_similarity_id(auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None, similarity_id: str, project_ids: List[str] = None, scan_id: str = None)
    assert result is not None


def test_predicate_severity_and_state_by_similiarty_id_and_project_id():
    result = predicate_severity_and_state_by_similiarty_id_and_project_id(request_body: List[dict], auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None)
    assert result is not None


def test_update_predicate_comment_by_predicate_id():
    result = update_predicate_comment_by_predicate_id(request_body: List[dict], auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None)
    assert result is not None


def test_recalculate_summary_counters():
    result = recalculate_summary_counters(request_body: dict, auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None)
    assert result is not None


def test_delete_a_predicate_history():
    result = delete_a_predicate_history(auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None, similarity_id: str, project_id: str, predicate_id: str)
    assert result is not None

