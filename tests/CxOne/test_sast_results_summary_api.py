import pytest
from CheckmarxPythonSDK.CxOne import (
    get_sast_aggregate_results,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def test_get_sast_aggregate_results():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    response = get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=["QUERY"],
    )
    assert response is not None
