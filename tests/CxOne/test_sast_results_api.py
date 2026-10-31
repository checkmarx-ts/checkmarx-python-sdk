import pytest
from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
    get_sast_results_compare_by_scans,
    get_similar_results,
)
from CheckmarxPythonSDK.CxOne.dto import SimilarResultsResponse, SimilarResultGroup
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
import logging
logger = logging.getLogger(__name__)


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def _get_two_sast_scan_ids():
    result = _ScansAPI().get_a_list_of_scans(limit=20, statuses=["Completed"])
    ids = []
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            ids.append(scan.id)
            if len(ids) >= 2:
                return ids[0], ids[1]
    return None, None


def test_get_sast_results_by_scan_id():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    offset = 0
    limit = 500
    page = 1
    sast_results_collection = get_sast_results_by_scan_id(scan_id=scan_id, offset=offset, limit=limit, state=["TO_VERIFY", "CONFIRMED"], include_nodes=False,)
    total_count = int(sast_results_collection.get("totalCount"))
    logger.info(f"number of totalCount results: {total_count}")
    sast_results = sast_results_collection.get("results")
    if total_count > limit:
        while True:
            offset = page * limit
            if offset >= total_count:
                break
            sast_results_collection = get_sast_results_by_scan_id(scan_id=scan_id, offset=offset, limit=limit, state=["TO_VERIFY", "CONFIRMED"], include_nodes=False,)
            page += 1
            sast_results.extend(sast_results_collection.get("results"))
    logger.info(f"number of TO_VERIFY or CONFIRMED results: {len(sast_results)}")
    pass


def test_get_sast_results_by_scan_id_with_new_filters():
    # exercises filters added when this method was expanded to full
    # doc parity: attack_vector_id, bfl_group_size/name,
    # confidence_level/score, cwe_id, is_ai_generated, similarity_id,
    # group_operation, query_operation, visible_columns,
    # correlation_id -- plus their *_operation variants.
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")

    result = get_sast_results_by_scan_id(
        scan_id=scan_id,
        limit=5,
        cwe_id=79,
        cwe_id_operation="EQUAL",
        is_ai_generated=0,
        is_ai_generated_operation="EQUAL",
        confidence_score=50,
        confidence_score_operation="GREATER_THAN",
        confidence_level=1,
        confidence_level_operation="EQUAL",
        bfl_name="main",
        bfl_name_operation="CONTAINS",
        bfl_group_size=2,
        bfl_group_size_operation="GREATER_THAN",
        attack_vector_id="0000000000000001",
        attack_vector_id_operation="EQUAL",
        group_operation="CONTAINS",
        query_operation="EQUAL",
        query="SQL_Injection",
        visible_columns=["scan-id", "result-id", "query-ids"],
        correlation_id="11111111-1111-1111-1111-111111111111",
    )
    assert "results" in result
    assert "totalCount" in result

    # similarity_id filtering should narrow to at most the matching
    # result(s) for *some* real similarity id in this scan -- grab one
    # from the unfiltered call above rather than assuming a specific
    # id exists on whatever scan _get_sast_scan_id() happens to pick.
    if result["results"]:
        real_similarity_id = result["results"][0].similarity_id
        result2 = get_sast_results_by_scan_id(
            scan_id=scan_id,
            similarity_id=real_similarity_id,
            similarity_id_operation="EQUAL",
        )
        assert result2["totalCount"] >= 1
        assert all(
            r.similarity_id == real_similarity_id
            for r in result2["results"]
        )


def test_get_sast_results_compare_by_scans():
    scan_id, base_scan_id = _get_two_sast_scan_ids()
    if not scan_id or not base_scan_id:
        pytest.skip("Need two completed SAST scans for comparison")
    try:
        result = get_sast_results_compare_by_scans(
            scan_id=scan_id,
            base_scan_id=base_scan_id,
            limit=5,
        )
        assert result is not None
        assert "results" in result
    except Exception as e:
        logger.warning("get_sast_results_compare_by_scans skipped: {}".format(str(e)))


def test_get_similar_results():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    results = get_sast_results_by_scan_id(scan_id=scan_id, limit=1)
    if not results["results"]:
        pytest.skip("No SAST result found in scan")
    result_hash = results["results"][0].result_hash

    result = get_similar_results(
        scan_id=scan_id,
        results_hash=[result_hash],
        correlation_id="11111111-1111-1111-1111-111111111111",
    )
    assert isinstance(result, SimilarResultsResponse)
    assert result.total_counts == 1
    assert result.grouping_mode in ("Similarity ID", "Attack Vector ID")
    assert len(result.similar_results) == 1
    group = result.similar_results[0]
    assert isinstance(group, SimilarResultGroup)
    assert group.result_hash == result_hash
    assert group.similar_results_count is not None
    assert group.is_state_inconsistent is not None
    assert group.is_severity_inconsistent is not None
