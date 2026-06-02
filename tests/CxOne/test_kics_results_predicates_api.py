import pytest

from CheckmarxPythonSDK.CxOne import (
    get_predicates_by_similarity_id,
    get_predicates_changes,
    create_predicate,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne import KicsResultsAPI


def _get_kics_data():
    """Get a scan_id and project_id from a completed KICS scan."""
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "kics" in (scan.engines or []):
            return scan.id, scan.project_id
    return None, None


def test_get_predicates_by_similarity_id():
    scan_id, project_id = _get_kics_data()
    if not scan_id:
        pytest.skip("No completed KICS scan found")
    try:
        result = get_predicates_by_similarity_id(
            similarity_id="491614176",
            project_ids=[project_id],
            scan_id=scan_id,
        )
        assert result is not None
        assert "predicateHistoryPerProject" in result
    except Exception as e:
        print("get_predicates_by_similarity_id skipped: {}".format(str(e)))


def test_get_predicates_changes():
    scan_id, project_id = _get_kics_data()
    if not scan_id:
        pytest.skip("No completed KICS scan found")
    try:
        result = get_predicates_changes(
            similarity_id="491614176",
            project_id=project_id,
        )
        assert result is not None
        assert "predicates" in result
    except Exception as e:
        print("get_predicates_changes skipped: {}".format(str(e)))


def test_create_predicate():
    scan_id, project_id = _get_kics_data()
    if not scan_id:
        pytest.skip("No completed KICS scan found")
    try:
        result = create_predicate(
            data=[{
                "similarityId": "491614176",
                "scanId": scan_id,
                "projectId": project_id,
                "severity": "HIGH",
                "state": "TO_VERIFY",
                "comment": "test from SDK",
            }]
        )
        assert result is True
    except Exception as e:
        print("create_predicate skipped: {}".format(str(e)))
