import pytest

from CheckmarxPythonSDK.CxOne import (
    get_kics_scans_metadata,
    get_kics_scan_metadata,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_kics_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "kics" in (scan.engines or []):
            return scan.id
    return None


def test_get_kics_scans_metadata():
    scan_id = _get_kics_scan_id()
    if not scan_id:
        pytest.skip("No completed KICS scan found")
    result = get_kics_scans_metadata(scan_ids=[scan_id])
    assert result is not None
    assert "scans" in result


def test_get_kics_scan_metadata():
    scan_id = _get_kics_scan_id()
    if not scan_id:
        pytest.skip("No completed KICS scan found")
    result = get_kics_scan_metadata(scan_id=scan_id)
    assert result is not None
    assert "scanId" in result
