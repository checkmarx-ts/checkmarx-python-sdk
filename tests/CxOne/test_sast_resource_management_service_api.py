from CheckmarxPythonSDK.CxOne import (
    get_sast_scan_allocation_info,
    delete_sast_scan,
    get_sast_scans,
)


def test_get_sast_scan_allocation_info():
    # response is 502
    scan_id = "edcba8aa-2498-4d80-b4e5-4d83ff85930b"
    result = get_sast_scan_allocation_info(scan_id)
    assert result is not None


def test_delete_sast_scan():
    # response is 502
    scan_id = "edcba8aa-2498-4d80-b4e5-4d83ff85930b"
    result = delete_sast_scan(scan_id)
    assert result is not None


def test_get_sast_scans():
    # response is 502
    result = get_sast_scans()
    assert result is not None
