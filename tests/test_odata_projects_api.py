from CheckmarxPythonSDK.CxRestAPISDK import (ProjectsAPI, ScansAPI)
from CheckmarxPythonSDK.CxODataApiSDK import (
    get_top_n_projects_by_risk_score,
    get_top_n_projects_by_last_scan_duration,
    get_all_projects_with_their_last_scan_and_the_high_vulnerabilities,
    get_projects_that_have_high_vulnerabilities_in_the_last_scan,
    get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team,
    get_count_of_the_projects_in_the_system,
    get_all_projects_with_a_custom_field_that_has_a_specific_value,
    get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information,
    get_presets_associated_with_each_project,
    get_all_projects_that_are_set_up_with_a_non_standard_configuration,
    get_all_projects_id_name,
    get_all_projects_id_name_and_team_id_name,
)

project_name = "jvl_git"
scans_api = ScansAPI()
projects_api = ProjectsAPI()
project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name=project_name)


def test_get_top_n_projects_by_risk_score():
    number_of_projects = 10
    r = get_top_n_projects_by_risk_score(number_of_projects=number_of_projects)

    assert r is not None


def test_get_top_n_projects_by_last_scan_duration():
    number_of_projects = 10
    r = get_top_n_projects_by_last_scan_duration(number_of_projects=number_of_projects)

    assert r is not None


def test_get_all_projects_with_their_last_scan_and_the_high_vulnerabilities():
    r = get_all_projects_with_their_last_scan_and_the_high_vulnerabilities()
    assert r is not None


def test_get_projects_that_have_high_vulnerabilities_in_the_last_scan():
    r = get_projects_that_have_high_vulnerabilities_in_the_last_scan()
    assert r is not None


def test_get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team():
    r = get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id=1, start_date='2001-01-01', end_date='2020-11-18'
    )
    assert r is not None


def test_get_count_of_the_projects_in_the_system():
    count = get_count_of_the_projects_in_the_system()
    assert count >= 0


def test_get_all_projects_with_a_custom_field_that_has_a_specific_value():
    project_manager = 'Joe'
    projects = get_all_projects_with_a_custom_field_that_has_a_specific_value(
        field_name='projectManager', field_value=project_manager)

    assert len(projects) > 0


def test_get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information():
    projects = get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(
        field_name='projectManager')

    assert len(projects) > 0


def test_get_presets_associated_with_each_project():
    projects = get_presets_associated_with_each_project()

    assert len(projects) > 0


def test_get_all_projects_that_are_set_up_with_a_non_standard_configuration():
    projects = get_all_projects_that_are_set_up_with_a_non_standard_configuration()

    assert len(projects) >= 0


def test_get_all_projects_id_name():
    r = get_all_projects_id_name()
    assert r is not None


def test_get_all_projects_id_name_and_team_id_name():
    r = get_all_projects_id_name_and_team_id_name()
    assert r is not None

