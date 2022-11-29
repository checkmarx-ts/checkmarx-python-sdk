from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
)


def test_get_sast_results_by_scan_id():
    response = get_sast_results_by_scan_id(scan_id="353d9a5d-cf52-4384-8516-e31d7447ead1")
    assert response is not None
