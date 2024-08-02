from CheckmarxPythonSDK.CxOne import (
    get_metadata_of_scans,
    get_metadata_of_scan,
    get_engine_metrics_of_scan,
    get_engine_versions_of_scan,
)


def test_get_metadata_of_scans():
    # result = get_metadata_of_scans(scan_ids=["ae8ae620-06bb-4c16-bb15-809270e0ccc6"])
    # assert result is not None
    result = get_metadata_of_scans(scan_ids=["ae8ae620-06bb-4c16-bb15-809270e0ccc6",
                                             "09ad7faf-74e5-415b-b81a-f4f209b736a4"])
    assert result is not None


def test_get_metadata_of_scan():
    result = get_metadata_of_scan(scan_id="ae8ae620-06bb-4c16-bb15-809270e0ccc6")
    assert result is not None


def test_get_engine_metrics_of_scan():
    result = get_engine_metrics_of_scan(scan_id="ae8ae620-06bb-4c16-bb15-809270e0ccc6")
    assert result is not None


def test_get_engine_versions_of_scan():
    # result = get_engine_versions_of_scan(scan_ids=["ae8ae620-06bb-4c16-bb15-809270e0ccc6"])
    # assert result is not None
    result = get_engine_versions_of_scan(scan_ids=["ae8ae620-06bb-4c16-bb15-809270e0ccc6",
                                                   "09ad7faf-74e5-415b-b81a-f4f209b736a4"])
    assert result is not None
