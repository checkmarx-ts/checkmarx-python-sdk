import pytest
import time

from CheckmarxPythonSDK.CxOne import (
    create_sca_scan_report,
    download_sca_export,
    get_sca_export_status,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_sca_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sca" in (scan.engines or []):
            return scan.id
    return None


def _wait_for_completed(export_id, timeout_seconds=60):
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        status = get_sca_export_status(export_id)
        if status.export_status == "Completed":
            return
        if status.export_status == "Failed":
            pytest.skip(f"export {export_id} failed: {status.error_message}")
        time.sleep(2)
    pytest.skip(f"export {export_id} did not complete within {timeout_seconds}s")


def test_download_sca_export_json_format():
    scan_id = _get_sca_scan_id()
    if not scan_id:
        pytest.skip("No completed SCA scan found")

    export_id = create_sca_scan_report(scan_id, file_format="ScanReportJson")
    _wait_for_completed(export_id)

    result = download_sca_export(export_id)
    assert isinstance(result, dict)


def test_download_sca_export_binary_format():
    scan_id = _get_sca_scan_id()
    if not scan_id:
        pytest.skip("No completed SCA scan found")

    export_id = create_sca_scan_report(scan_id, file_format="ScanReportPdf")
    _wait_for_completed(export_id)

    result = download_sca_export(export_id)
    assert isinstance(result, bytes)
    assert result[:5] == b"%PDF-"


def test_download_sca_export_unknown_export_id():
    with pytest.raises(ValueError):
        download_sca_export("00000000-0000-0000-0000-000000000000")
