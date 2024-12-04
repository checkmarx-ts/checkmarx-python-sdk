from CheckmarxPythonSDK.CxOne import (
    get_sast_aggregate_results,
)


def test_get_sast_aggregate_results():
    response = get_sast_aggregate_results(
        scan_id="eff7552e-b7a4-4576-a1be-63e8236b6ab6",
        group_by_field=["QUERY"],
    )
    assert response is not None
