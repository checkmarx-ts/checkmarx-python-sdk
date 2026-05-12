import pytest
from CheckmarxPythonSDK.CxOne import (
    get_metadata_of_scans,
    get_metadata_of_scan,
    get_engine_metrics_of_scan,
    get_engine_versions_of_scan,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def _get_scan_id(engine=None):
    """Return a completed scan ID, optionally filtered by engine type."""
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if engine is None or engine in (scan.engines or []):
            return scan.id
    return None


def test_get_metadata_of_scans():
    scan_id_1 = _get_sast_scan_id()
    if not scan_id_1:
        pytest.skip("No completed SAST scan found")
    result = get_metadata_of_scans(scan_ids=[scan_id_1])
    assert result is not None


def test_get_metadata_of_scan():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = get_metadata_of_scan(scan_id=scan_id)
    assert result is not None


def test_get_engine_metrics_of_scan():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = get_engine_metrics_of_scan(scan_id=scan_id)
    assert result is not None


def test_get_engine_versions_of_scan():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = get_engine_versions_of_scan(scan_ids=[scan_id])
    assert result is not None
