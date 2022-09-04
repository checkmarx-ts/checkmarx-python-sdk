from CheckmarxPythonSDK.CxRestAPISDK import (ProjectsAPI, ScansAPI)
from CheckmarxPythonSDK.CxODataApiSDK import (
    get_all_data_for_a_specific_scan_id,
    get_number_of_loc_scanned_for_a_specific_scan,
    get_number_of_loc_scanned_for_all_scan,
    get_last_scan_id_of_a_project,
    get_last_full_scan_id_of_a_project,
    get_last_scan_of_a_project,
    get_last_full_scan_of_a_project,
    get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project,
    get_the_state_of_each_scan_result_since_a_specific_date_for_a_project,
    get_all_scan_id_of_a_project,
)

project_name = "jvl_git"
projects_api = ProjectsAPI()
project_id = projects_api.get_project_id_by_project_name_and_team_full_name(
    project_name=project_name, team_full_name="/CxServer"
)


def test_get_all_data_for_a_specific_scan_id():

    scan_id = get_last_scan_id_of_a_project(project_id=project_id)

    r = get_all_data_for_a_specific_scan_id(scan_id=scan_id)

    assert r is not None


def test_retrieve_number_of_loc_scanned_for_a_specific_scan():
    scan_id = get_last_scan_id_of_a_project(project_id=project_id)

    r = get_number_of_loc_scanned_for_a_specific_scan(scan_id=scan_id)

    assert r > 1


def test_get_number_of_loc_scanned_for_all_scan():

    loc_id_pair_list = get_number_of_loc_scanned_for_all_scan()

    assert len(loc_id_pair_list) > 0


def test_get_last_scan_id_of_a_project():

    r = get_last_scan_id_of_a_project(project_id=project_id)

    assert r is not None


def test_get_last_scan_of_a_project():

    r = get_last_scan_of_a_project(project_id=project_id)

    assert r is not None


def test_get_last_full_scan_id_of_a_project():

    r = get_last_full_scan_id_of_a_project(project_id=project_id)

    assert r > 1


def test_get_last_full_scan_of_a_project():

    r = get_last_full_scan_of_a_project(project_id=project_id)

    assert r is not None


def test_get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project():

    r = get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
        project_id=project_id, start_date='2020-01-01', end_date='2020-11-17'
    )

    assert r is not None


def test_get_the_state_of_each_scan_result_since_a_specific_date_for_a_project():

    r = get_the_state_of_each_scan_result_since_a_specific_date_for_a_project(project_id=project_id,
                                                                              start_date='2019-01-01')

    assert r is not None


def test_get_scan_id_list_for_one_project():

    scan_id_list = get_all_scan_id_of_a_project(project_id=project_id)

    assert len(scan_id_list) > 0
