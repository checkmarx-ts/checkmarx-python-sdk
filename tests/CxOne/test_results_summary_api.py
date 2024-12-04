from CheckmarxPythonSDK.CxOne import (
    get_summary_for_many_scans,
)


def test_get_summary_for_many_scans():
    response = get_summary_for_many_scans(scan_ids=["eff7552e-b7a4-4576-a1be-63e8236b6ab6"])
    assert response is not None
