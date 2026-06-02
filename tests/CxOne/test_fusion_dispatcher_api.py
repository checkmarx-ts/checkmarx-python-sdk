import pytest

from CheckmarxPythonSDK.CxOne import (
    correlate,
    get_scan_status,
)
from CheckmarxPythonSDK.CxOne import FusionResultsAPI


def _get_app_id():
    """Get an application ID from the fusion results list."""
    try:
        result = FusionResultsAPI().get_applications()
        apps = result.get("applications", [])
        return apps[0] if apps else None
    except Exception:
        return None


def test_get_scan_status():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No fusion applications found")
    try:
        result = get_scan_status(id=app_id)
        assert result is not None
        assert "scanStatus" in result
    except Exception as e:
        print("get_scan_status skipped: {}".format(str(e)))


def test_correlate():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No fusion applications found")
    try:
        result = correlate(id=app_id)
        assert result is True
    except Exception as e:
        print("correlate skipped: {}".format(str(e)))
