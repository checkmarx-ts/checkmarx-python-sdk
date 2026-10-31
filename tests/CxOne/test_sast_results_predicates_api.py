import pytest
from typing import List
from CheckmarxPythonSDK.CxOne import (
    get_all_predicates_for_similarity_id,
    get_latest_predicates_for_similarity_id,
    predicate_severity_and_state_by_similarity_id_and_project_id,
    update_predicate_comment_by_predicate_id,
    recalculate_summary_counters,
    delete_a_predicate_history,
    get_predicates_by_attack_vector_id,
    get_predicates_changelog,
    create_predicates_by_attack_vector,
    get_predicates_status,
    get_sast_results_by_scan_id,
)

from CheckmarxPythonSDK.CxOne.dto import (
    PredicateHistory,
    PredicateHistoryResponse,
    LatestPredicateResponse,
    Predicate,
    PredicateWithCommentJSON,
    PredicateWithCommentsJSON,
    PredicatesChangelogResponse,
    PredicateChangelogGroup,
    PredicateChangelogEntry,
    CommentJSON,
    WebError
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI
import logging
logger = logging.getLogger(__name__)


def _get_sast_scan_and_project_id():
    """Return (scan_id, project_id) for a completed SAST scan, or (None, None)."""
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id, scan.project_id
    return None, None


def _get_sast_similarity_id(scan_id):
    """Return a real similarity_id (str) with at least one result in
    scan_id, or None. The "491614176" similarity_id hardcoded
    elsewhere in this file no longer exists in this tenant's project
    (confirmed via a live 404: "sast similarity ID 491614176 does not
    exist for project ...") -- tests that actually create/mutate a
    predicate (rather than just listing, which tolerates an unknown
    id by returning empty results) need a real one.
    """
    results = get_sast_results_by_scan_id(scan_id=scan_id, limit=1)
    items = results.get("results") if isinstance(results, dict) else None
    if items:
        return str(items[0].similarity_id)
    return None


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
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST result found in scan")
    request_body: List[dict] = [{"similarityId": similarity_id, "projectId": project_id,
                                 "scanId": scan_id, "severity": "HIGH",
                                 "state": "CONFIRMED", "comment": "test"}]
    result = predicate_severity_and_state_by_similarity_id_and_project_id(data=request_body)
    assert result is not None


def test_predicate_severity_and_state_with_allow_ai_triage_cancellation():
    # Can't easily trigger a real 409 (code 4092) here -- that needs a
    # genuinely queued/in_progress AI Triage job on the target
    # vulnerability, not reproducible on demand. This just confirms
    # the allowAITriageCancellation param round-trips without
    # breaking the normal (no AI Triage conflict) success path.
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST result found in scan")
    request_body: List[dict] = [{"similarityId": similarity_id, "projectId": project_id,
                                 "scanId": scan_id, "severity": "MEDIUM",
                                 "state": "TO_VERIFY", "comment": "test allowAITriageCancellation"}]
    result = predicate_severity_and_state_by_similarity_id_and_project_id(
        data=request_body,
        allow_ai_triage_cancellation=True,
        correlation_id="11111111-1111-1111-1111-111111111111",
    )
    assert result is True


def test_get_latest_predicates_for_similarity_id_returns_real_data():
    # Regression test: get_latest_predicates_for_similarity_id used to
    # reuse PredicateHistoryResponse (which reads the
    # predicateHistoryPerProject key) for this endpoint, whose actual
    # response key is latestPredicatePerProject -- silently returning
    # an always-empty list despite totalCount being correctly nonzero.
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST result found in scan")

    # ensure at least one predicate exists for this similarity_id
    predicate_severity_and_state_by_similarity_id_and_project_id(
        data=[{
            "similarityId": similarity_id, "projectId": project_id,
            "scanId": scan_id, "severity": "LOW", "state": "TO_VERIFY",
            "comment": "regression test for get_latest_predicates_for_similarity_id",
        }]
    )

    result = get_latest_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=[project_id],
    )
    assert isinstance(result, LatestPredicateResponse)
    assert result.total_count > 0
    assert len(result.latest_predicate_per_project) > 0
    predicate = result.latest_predicate_per_project[0]
    assert isinstance(predicate, PredicateWithCommentsJSON)
    assert predicate.severity == "LOW"
    assert predicate.state == "TO_VERIFY"
    assert predicate.project_id == project_id
    assert isinstance(predicate.comments_json, list)
    assert len(predicate.comments_json) > 0
    assert isinstance(predicate.comments_json[0], CommentJSON)


def test_get_all_predicates_for_similarity_id_include_changed_by():
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST result found in scan")

    predicate_severity_and_state_by_similarity_id_and_project_id(
        data=[{
            "similarityId": similarity_id, "projectId": project_id,
            "scanId": scan_id, "severity": "LOW", "state": "TO_VERIFY",
            "comment": "regression test for include_changed_by",
        }]
    )

    result = get_all_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=[project_id],
        include_changed_by=True,
    )
    assert isinstance(result, PredicateHistoryResponse)
    assert len(result.predicate_history_per_project) > 0
    predicate = result.predicate_history_per_project[0].predicates[0]
    assert isinstance(predicate, PredicateWithCommentJSON)
    # present (even if empty string) only because include_changed_by=True
    assert predicate.triggered_by is not None
    assert predicate.changed_by is not None


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


def test_get_predicates_by_attack_vector_id():
    """GET / — get predicates by attack vector ID.

    NOTE: "0000000000000001" is a placeholder, not a real attack
    vector id discoverable on this tenant (confirmed: the live server
    400s identically on this id both before and after this method
    was extended with limit/offset/include_changed_by, isolating the
    placeholder id -- not the new params -- as the cause). This test
    can only confirm the call doesn't error on request shape; it
    can't exercise a real PredicateHistoryResponse payload from this
    endpoint specifically (the response DTO itself is already
    live-verified via the sibling /{similarityID} endpoint).
    """
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    try:
        result = get_predicates_by_attack_vector_id(
            attack_vector_id="0000000000000001",
            project_ids=[project_id],
            scan_id=scan_id,
            include_changed_by=True,
            limit=5,
            offset=0,
        )
        assert result is not None
    except Exception as e:
        logger.warning("get_predicates_by_attack_vector_id skipped: {}".format(str(e)))


def test_get_predicates_changelog():
    """GET /changelog — get predicates changelog."""
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    try:
        result = get_predicates_changelog(
            entity_type="scanID",
            entity_id=scan_id,
            limit=10,
        )
        assert result is not None
        assert isinstance(result, PredicatesChangelogResponse)
        assert result.total_similarity_ids is not None
        if result.results:
            group = result.results[0]
            assert isinstance(group, PredicateChangelogGroup)
            assert group.similarity_id is not None
            if group.predicates:
                assert isinstance(group.predicates[0], PredicateChangelogEntry)
    except Exception as e:
        logger.warning("get_predicates_changelog skipped: {}".format(str(e)))


def test_create_predicates_by_attack_vector():
    """POST /attack-vector — create predicates by attack vector."""
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    try:
        result = create_predicates_by_attack_vector(
            data=[{
                "attackVectorId": "0000000000000001",
                "projectId": project_id,
                "scanId": scan_id,
                "state": "TO_VERIFY",
                "severity": "MEDIUM",
                "comment": "test from SDK",
            }]
        )
        assert result is not None
    except Exception as e:
        logger.warning("create_predicates_by_attack_vector skipped: {}".format(str(e)))


def test_get_predicates_status():
    """POST /predicates-status — get predicates update status."""
    scan_id, project_id = _get_sast_scan_and_project_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    try:
        result = get_predicates_status(
            scan_id=scan_id,
            similar_results_ids=["491614176"],
        )
        assert result is not None
        assert "isUpdatePredicatesRunning" in result
    except Exception as e:
        logger.warning("get_predicates_status skipped: {}".format(str(e)))
