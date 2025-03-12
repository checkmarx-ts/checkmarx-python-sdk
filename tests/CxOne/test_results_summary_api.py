from CheckmarxPythonSDK.CxOne import (
    get_summary_for_many_scans,
)


def test_get_summary_for_many_scans():
    response = get_summary_for_many_scans(scan_ids=["63c76f1a-733c-49c8-97c8-4fbc6c0dcfe1"], include_queries=True)
    assert response is not None
