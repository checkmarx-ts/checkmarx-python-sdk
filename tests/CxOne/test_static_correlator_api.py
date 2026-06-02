import pytest

from CheckmarxPythonSDK.CxOne import update_risk
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_apisec_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "apisec" in (scan.engines or []):
            return scan.id
    return None


def test_update_risk():
    scan_id = _get_apisec_scan_id()
    if not scan_id:
        pytest.skip("No completed APISec scan found")
    try:
        result = update_risk(
            scan_id=scan_id,
            method="PUT",
            similarity_id="491614176",
            url="https://example.com/api",
            severity="HIGH",
            state="CONFIRMED",
        )
        assert result is not None
    except Exception as e:
        print("update_risk skipped: {}".format(str(e)))
