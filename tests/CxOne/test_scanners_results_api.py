import pytest
from CheckmarxPythonSDK.CxOne import get_all_scanners_results_by_scan_id
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_scan_id(engine=None):
    """Return a completed scan ID, optionally filtered by engine type."""
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if engine is None or engine in (scan.engines or []):
            return scan.id
    return None


def test_get_all_scanners_results_by_scan_id():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No completed scan found")
    response = get_all_scanners_results_by_scan_id(scan_id=scan_id, limit=500)
    assert response is not None
