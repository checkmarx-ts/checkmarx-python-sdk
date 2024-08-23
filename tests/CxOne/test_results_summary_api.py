from CheckmarxPythonSDK.CxOne import (
    get_summary_for_many_scans,
)


def test_get_summary_for_many_scans():
    response = get_summary_for_many_scans(scan_ids=["09ad7faf-74e5-415b-b81a-f4f209b736a4"])
    assert response is not None
