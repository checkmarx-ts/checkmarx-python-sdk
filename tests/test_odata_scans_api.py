from CheckmarxPythonSDK.CxRestAPISDK import (ProjectsAPI, ScansAPI)
from CheckmarxPythonSDK.CxODataApiSDK import ScansODataAPI

project_name = "jvl_git"
scans_api = ScansAPI()
projects_api = ProjectsAPI()
project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name=project_name)


def test_retrieve_all_data_for_a_specific_scan_id():
    scans_odata_api = ScansODataAPI()

    scan_id = scans_api.get_last_scan_id_of_a_project(project_id=project_id, only_finished_scans=True)

    r = scans_odata_api.retrieve_all_data_for_a_specific_scan_id(scan_id=scan_id)

    assert r is not None


def test_retrieve_number_of_loc_scanned_for_a_specific_scan():
    scans_odata_api = ScansODataAPI()

    scan_id = scans_api.get_last_scan_id_of_a_project(project_id=project_id, only_finished_scans=True)

    r = scans_odata_api.retrieve_number_of_loc_scanned_for_a_specific_scan(scan_id=scan_id)

    assert r > 1
