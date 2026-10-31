import pytest

from CheckmarxPythonSDK.CxOne import get_compare_status
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne.dto import (
    SastComparisonStatus,
    SeverityStatusCounter,
    CompareStatusCount,
    ScanSeverityCounters,
)


def _get_two_sast_scan_ids_same_project():
    # The doc says this endpoint compares "two scans of a single
    # project" -- group by project_id rather than just taking the
    # first two SAST scans found (which could belong to different
    # projects).
    result = _ScansAPI().get_a_list_of_scans(limit=30, statuses=["Completed"])
    by_project = {}
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            by_project.setdefault(scan.project_id, []).append(scan.id)
    for scan_ids in by_project.values():
        if len(scan_ids) >= 2:
            return scan_ids[0], scan_ids[1]
    return None, None


def test_get_compare_status():
    scan_id, base_scan_id = _get_two_sast_scan_ids_same_project()
    if not scan_id or not base_scan_id:
        pytest.skip("Need two completed SAST scans in the same project")
    result = get_compare_status(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        evaluation_status=True,
        correlation_id="11111111-1111-1111-1111-111111111111",
    )
    assert isinstance(result, SastComparisonStatus)
    assert isinstance(result.scan_counters, ScanSeverityCounters)
    assert isinstance(result.base_scan_counters, ScanSeverityCounters)
    assert len(result.severity_status_counters) > 0
    group = result.severity_status_counters[0]
    assert isinstance(group, SeverityStatusCounter)
    assert group.severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")
    assert len(group.results) > 0
    assert isinstance(group.results[0], CompareStatusCount)
    assert group.results[0].status in ("NEW", "RECURRENT", "FIXED")
