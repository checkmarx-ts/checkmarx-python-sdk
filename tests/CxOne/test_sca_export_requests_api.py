import pytest

from CheckmarxPythonSDK.CxOne import create_sca_scan_report, get_sca_scan_report
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne.dto import ExportParametersSbom, ExportParametersScanReport


def _get_sca_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sca" in (scan.engines or []):
            return scan.id
    return None


def test_create_sca_scan_report_default_behavior():
    # no file_format/export_parameters -- must behave exactly as before
    # this method was parameterized (ScanReportJson + the same 6 flags)
    scan_id = _get_sca_scan_id()
    if not scan_id:
        pytest.skip("No completed SCA scan found")

    export_id = create_sca_scan_report(scan_id)
    assert export_id is not None

    result = get_sca_scan_report(export_id)
    assert isinstance(result, dict)
    assert "RiskReportSummary" in result or "Packages" in result


def test_create_sca_scan_report_sbom_format():
    scan_id = _get_sca_scan_id()
    if not scan_id:
        pytest.skip("No completed SCA scan found")

    export_id = create_sca_scan_report(
        scan_id,
        file_format="CycloneDxJson",
        export_parameters=ExportParametersSbom(hideDevAndTestDependencies=True),
    )
    assert export_id is not None

    result = get_sca_scan_report(export_id)
    assert isinstance(result, dict)


def test_create_sca_scan_report_pdf_format_returns_bytes():
    scan_id = _get_sca_scan_id()
    if not scan_id:
        pytest.skip("No completed SCA scan found")

    export_id = create_sca_scan_report(
        scan_id,
        file_format="ScanReportPdf",
        export_parameters=ExportParametersScanReport(),
    )
    assert export_id is not None

    result = get_sca_scan_report(export_id)
    assert isinstance(result, bytes)
    assert result[:5] == b"%PDF-"


def test_create_sca_scan_report_invalid_file_format():
    with pytest.raises(ValueError):
        create_sca_scan_report("any-scan-id", file_format="NotARealFormat")
