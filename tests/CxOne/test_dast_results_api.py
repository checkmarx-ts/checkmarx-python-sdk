import pytest

from CheckmarxPythonSDK.CxOne import (
    get_environments, get_scans, get_results, get_result_info,
)
from CheckmarxPythonSDK.CxOne.dto import (
    DastResultsCollection, DastResult, DastResultsFilter,
    DastResultStatus, DastResultsSortBy, DastResultDetail,
)


def _find_scan_with_results():
    """Return a scan_id from any scan that has results, or None."""
    envs = get_environments()
    for env in envs.environments:
        if not env.last_scan_id:
            continue
        scans = get_scans(environment_id=env.environment_id, to=10)
        for scan in scans.scans:
            if scan.has_results:
                return scan.scan_id
    return None


def test_get_results():
    scan_id = _find_scan_with_results()
    if not scan_id:
        pytest.skip("no scan with results on this tenant")
    coll = get_results(scan_id=scan_id, per_page=2)
    assert isinstance(coll, DastResultsCollection)
    assert coll.total is not None and coll.total >= 1
    assert coll.pages_number is not None
    assert isinstance(coll.results, list) and coll.results
    r = coll.results[0]
    assert isinstance(r, DastResult)
    assert r.id is not None
    assert r.severity is not None


def test_get_results_with_filter():
    scan_id = _find_scan_with_results()
    if not scan_id:
        pytest.skip("no scan with results on this tenant")
    # Filter by status=Recurrent (saw this status in the live data).
    coll = get_results(
        scan_id=scan_id,
        filter_=DastResultsFilter(status=DastResultStatus.RECURRENT),
        per_page=5,
    )
    assert isinstance(coll, DastResultsCollection)
    # All returned rows should have status Recurrent.
    for r in coll.results:
        assert r.status == DastResultStatus.RECURRENT or r.status == "Recurrent"


def test_get_result_info():
    scan_id = _find_scan_with_results()
    if not scan_id:
        pytest.skip("no scan with results on this tenant")
    coll = get_results(scan_id=scan_id, per_page=1)
    if not coll.results:
        pytest.skip("scan has no results")
    result_id = coll.results[0].id
    detail = get_result_info(result_id=result_id, scan_id=scan_id)
    assert isinstance(detail, DastResultDetail)
    assert detail.id == result_id
    # Detail-only fields should be present (compared to the list view).
    assert detail.solution is not None
    assert detail.description is not None


def test_get_results_with_sort():
    scan_id = _find_scan_with_results()
    if not scan_id:
        pytest.skip("no scan with results on this tenant")
    coll = get_results(
        scan_id=scan_id,
        sort_by=[DastResultsSortBy.SEVERITY],
        per_page=10,
    )
    assert isinstance(coll, DastResultsCollection)
