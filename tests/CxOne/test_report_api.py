import pytest

from CheckmarxPythonSDK.CxOne import (
    create_scan_report_v2, get_scan_report, get_a_list_of_scans,
)


def _find_scan_with_results():
    """Return a scan_id with multiple scanner engines, or None."""
    result = get_a_list_of_scans(limit=30, statuses=["Completed"])
    for scan in result.scans:
        engines = scan.engines or []
        if "sast" in engines or "sca" in engines:
            return scan.id, engines
    return None, None


def test_create_scan_report_v2_includes_critical_severity():
    """Confirmed live: the previous hardcoded severities filter
    (["high", "medium", "low", "information"]) silently excluded
    Critical -- the generated report's own reportFilters.filters
    confirmed "excluded": ["Critical"]. This asserts the fix: Critical
    is included by default and not reported as excluded.
    """
    scan_id, engines = _find_scan_with_results()
    if not scan_id:
        pytest.skip("No completed scan with SAST/SCA results found")
    scan_engines = [e for e in engines if e in ("sast", "sca", "iac")] or ["sast"]

    report_id = create_scan_report_v2(
        file_format="json", scan_engines=scan_engines, scan_id=scan_id,
    )
    assert report_id is not None

    report = get_scan_report(report_id=report_id)
    severity_filter = next(
        f for f in report["reportFilters"]["filters"]
        if f["filterName"] == "Severity"
    )
    assert "Critical" in severity_filter["included"]
    assert "Critical" not in severity_filter["excluded"]
