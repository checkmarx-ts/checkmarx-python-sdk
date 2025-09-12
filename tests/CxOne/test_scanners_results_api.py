from CheckmarxPythonSDK.CxOne import get_all_scanners_results_by_scan_id


def test_get_all_scanners_results_by_scan_id():
    response = get_all_scanners_results_by_scan_id(scan_id="62ce0be4-2058-4a6a-926e-69267d23bcd7", limit=500)
    assert response is not None
