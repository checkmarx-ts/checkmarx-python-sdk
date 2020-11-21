from CheckmarxPythonSDK.CxODataApiSDK import (
    get_results_for_a_specific_scan_id,
    get_the_query_that_was_run_for_a_particular_unique_scan_result,
    get_results_for_a_specific_scan_id_with_query_language_state,

    scan_results_group_by_query_id,
)


def test_get_results_for_a_specific_scan_id():
    scan_id = 1000012
    results = get_results_for_a_specific_scan_id(scan_id=scan_id)
    assert results is not None


def test_get_the_query_that_was_run_for_a_particular_unique_scan_result():
    scan_id = 1000012
    query_name = get_the_query_that_was_run_for_a_particular_unique_scan_result(result_id=1,
                                                                                scan_id=scan_id)
    assert query_name is not None


def test_get_results_for_a_specific_scan_id_with_query_language_state():

    r = get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=1000012,
        filter_false_positive=False
    )
    assert r is not None


def test_get_results_group_by_query_id():

    r = get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=1000012,
        filter_false_positive=False
    )

    r = scan_results_group_by_query_id(r)
    assert r is not None


def test_get_results_group_by_query_id_and_add_count_filter_false_positive():
    r = get_results_for_a_specific_scan_id_with_query_language_state(scan_id=1000012,
                                                                     filter_false_positive=True)
    r = scan_results_group_by_query_id(r)

    assert r is not None
