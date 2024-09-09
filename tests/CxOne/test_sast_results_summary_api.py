from CheckmarxPythonSDK.CxOne import (
    get_sast_aggregate_results,
)


def test_get_sast_aggregate_results():
    response = get_sast_aggregate_results(
        scan_id="09ad7faf-74e5-415b-b81a-f4f209b736a4",
        group_by_field=["LANGUAGE"],
    )
    assert response is not None
