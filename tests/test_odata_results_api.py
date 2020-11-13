from CheckmarxPythonSDK.CxODataApiSDK import ResultsODataAPI


def test_get_results_for_a_specific_scan_id():
    results_odata_api = ResultsODataAPI()
    scan_id = 1000012
    r = results_odata_api.get_results_for_a_specific_scan_id(scan_id=scan_id)
    assert r is not None


def test_retrieve_the_query_that_was_run_for_a_particular_unique_scan_result():
    results_odata_api = ResultsODataAPI()
    scan_id = 1000012
    r = results_odata_api.retrieve_the_query_that_was_run_for_a_particular_unique_scan_result(result_id=1,
                                                                                              scan_id=scan_id)
    assert r is not None


def test_get_results_for_a_specific_scan_id_with_query_language_state():
    results_odata_api = ResultsODataAPI()
    r = results_odata_api.get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=1000012,
        filter_false_positive=False
    )
    assert r is not None


def test_get_results_group_by_query_id():
    results_odata_api = ResultsODataAPI()
    r = results_odata_api.get_results_group_by_query_id(
        scan_id=1000012,
        filter_false_positive=False
    )
    assert r is not None


def test_get_results_group_by_query_id_and_add_count():
    results_odata_api = ResultsODataAPI()
    r = results_odata_api.get_results_group_by_query_id_and_add_count(scan_id=1000012, filter_false_positive=False)
    assert r is not None


def test_get_results_group_by_query_id_and_add_count_filter_false_positive():
    results_odata_api = ResultsODataAPI()
    r = results_odata_api.get_results_group_by_query_id_and_add_count(scan_id=1000012, filter_false_positive=True)
    assert r is not None
