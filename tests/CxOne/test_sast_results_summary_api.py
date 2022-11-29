from CheckmarxPythonSDK.CxOne import (
    get_summary_for_many_scans,
    get_sast_aggregate_results,
)


def test_get_summary_for_many_scans():
    response = get_summary_for_many_scans(scan_ids=["353d9a5d-cf52-4384-8516-e31d7447ead1"])
    assert response is not None


def test_get_sast_aggregate_results():
    response = get_sast_aggregate_results(
        scan_id="353d9a5d-cf52-4384-8516-e31d7447ead1",
        group_by_field=["LANGUAGE"],
    )
    assert response is not None
