from CheckmarxPythonSDK.CxRestAPISDK import (ProjectsAPI, ScansAPI)
from CheckmarxPythonSDK.CxODataApiSDK import (
    get_results_for_a_specific_scan_id,
    get_the_query_that_was_run_for_a_particular_unique_scan_result,
    get_results_for_a_specific_scan_id_with_query_language_state,
    get_results_for_a_specific_scan_id_with_similarity_ids,
    scan_results_group_by_query_id,
    get_number_of_results_for_a_specific_scan_id_with_result_state,
)

project_name = "jvl_git"
scans_api = ScansAPI()
projects_api = ProjectsAPI()
project_id = projects_api.get_project_id_by_project_name_and_team_full_name(
    project_name=project_name, team_full_name="/CxServer"
)

scan_id = scans_api.get_last_scan_id_of_a_project(project_id, only_finished_scans=True)


def test_get_results_for_a_specific_scan_id():
    results = get_results_for_a_specific_scan_id(scan_id=scan_id)
    assert results is not None


def test_get_the_query_that_was_run_for_a_particular_unique_scan_result():
    query_name = get_the_query_that_was_run_for_a_particular_unique_scan_result(result_id=1,
                                                                                scan_id=scan_id)
    assert query_name is not None


def test_get_results_for_a_specific_scan_id_with_query_language_state():

    r = get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=scan_id,
        filter_false_positive=False
    )
    assert r is not None


def test_get_results_group_by_query_id():

    r = get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=scan_id,
        filter_false_positive=False
    )

    r = scan_results_group_by_query_id(r)
    assert r is not None


def test_get_results_group_by_query_id_and_add_count_filter_false_positive():
    r = get_results_for_a_specific_scan_id_with_query_language_state(scan_id=scan_id,
                                                                     filter_false_positive=True)
    r = scan_results_group_by_query_id(r)

    assert r is not None


def test_get_results_for_a_specific_scan_id_with_similarity_ids():
    r = get_results_for_a_specific_scan_id_with_similarity_ids(
        scan_id=scan_id,
        similarity_ids=[2137433037, -1403228976]
    )
    assert r is not None


def test_get_similarity_ids_of_a_scan():
    def get_similarity_ids_of_a_scan():
        from CheckmarxPythonSDK.CxODataApiSDK.HttpRequests import get_request
        url = f"/Cxwebinterface/odata/v1/Scans(1000414)/Results?$select=SimilarityId,PathId"
        return get_request(relative_url=url)
    r = get_similarity_ids_of_a_scan()
    assert r is not None


def test_get_number_of_results_for_a_specific_scan_id_with_result_state():
    r = get_number_of_results_for_a_specific_scan_id_with_result_state(
        scan_id=scan_id, result_states=["NOT_EXPLOITABLE"]
    )
    assert r is not None
