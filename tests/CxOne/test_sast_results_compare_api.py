import pytest

from CheckmarxPythonSDK.CxOne import get_compare_status
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_two_sast_scan_ids():
    result = _ScansAPI().get_a_list_of_scans(limit=20, statuses=["Completed"])
    ids = []
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            ids.append(scan.id)
            if len(ids) >= 2:
                return ids[0], ids[1]
    return None, None


def test_get_compare_status():
    scan_id, base_scan_id = _get_two_sast_scan_ids()
    if not scan_id or not base_scan_id:
        pytest.skip("Need two completed SAST scans")
    result = get_compare_status(
        scan_id=scan_id, base_scan_id=base_scan_id
    )
    assert result is not None
    assert "severityStatusCounters" in result
