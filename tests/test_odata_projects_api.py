from CheckmarxPythonSDK.CxRestAPISDK import (ProjectsAPI, ScansAPI)
from CheckmarxPythonSDK.CxODataApiSDK import ProjectsODataAPI

project_name = "jvl_git"
scans_api = ScansAPI()
projects_api = ProjectsAPI()
project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name=project_name)


def test_get_top_n_projects_by_risk_score():
    project_odata_api = ProjectsODataAPI()

    number_of_projects = 10
    r = project_odata_api.get_top_n_projects_by_risk_score(number_of_projects=number_of_projects)

    assert r is not None


def test_get_top_n_projects_by_last_scan_duration():
    project_odata_api = ProjectsODataAPI()

    number_of_projects = 10
    r = project_odata_api.get_top_n_projects_by_last_scan_duration(number_of_projects=number_of_projects)

    assert r is not None


def test_get_all_projects_with_their_last_scan_and_the_high_vulnerabilities():
    project_odata_api = ProjectsODataAPI()
    r = project_odata_api.get_all_projects_with_their_last_scan_and_the_high_vulnerabilities()
    assert r is not None


def test_get_projects_that_have_high_vulnerabilities_in_the_last_scan():
    project_odata_api = ProjectsODataAPI()
    r = project_odata_api.get_projects_that_have_high_vulnerabilities_in_the_last_scan()
    assert r is not None


def test_get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team():
    p = ProjectsODataAPI()
    r = p.get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id=1, start_date='2001-01-01', end_date='2020-11-18'
    )
    assert r is not None


def test_get_count_of_the_projects_in_the_system():
    project_odata_api = ProjectsODataAPI()
    count = project_odata_api.get_count_of_the_projects_in_the_system()
    assert count >= 0


def test_get_all_projects_with_a_custom_field_that_has_a_specific_value():
    project_odata_api = ProjectsODataAPI()
    project_manager = 'Joe'
    projects = project_odata_api.get_all_projects_with_a_custom_field_that_has_a_specific_value(
        field_name='projectManager', field_value=project_manager)

    assert len(projects) > 0


def test_get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information():
    project_odata_api = ProjectsODataAPI()

    projects = project_odata_api.get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(
        field_name='projectManager')

    assert len(projects) > 0


def test_get_all_projects_id_name():
    project_odata_api = ProjectsODataAPI()
    r = project_odata_api.get_all_projects_id_name()
    assert r is not None
