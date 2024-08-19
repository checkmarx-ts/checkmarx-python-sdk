from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
)


def test_get_sast_results_by_scan_id():
    response = get_sast_results_by_scan_id(scan_id="ae8ae620-06bb-4c16-bb15-809270e0ccc6")
    assert response is not None
