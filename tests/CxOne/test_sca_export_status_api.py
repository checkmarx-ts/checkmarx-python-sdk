import pytest

from CheckmarxPythonSDK.CxOne import (
    create_sca_scan_report,
    get_sca_export_status,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne.dto import ScaExportStatus


def _get_sca_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sca" in (scan.engines or []):
            return scan.id
    return None


def test_get_sca_export_status():
    scan_id = _get_sca_scan_id()
    if not scan_id:
        pytest.skip("No completed SCA scan found")

    export_id = create_sca_scan_report(scan_id)
    status = get_sca_export_status(export_id)

    assert isinstance(status, ScaExportStatus)
    assert status.export_id == export_id
    assert status.export_status in ("Pending", "Exporting", "Completed", "Failed")
    if status.export_status == "Completed":
        assert status.file_url is not None


def test_get_sca_export_status_unknown_export_id():
    with pytest.raises(ValueError):
        get_sca_export_status("00000000-0000-0000-0000-000000000000")
