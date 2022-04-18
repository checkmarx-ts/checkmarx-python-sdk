from CheckmarxPythonSDK.CxAST import (
    create_a_project,
    get_a_list_of_projects,
    get_project_id_by_name,
    get_all_project_tags,
    get_last_scan_info,
    get_branches,
    get_a_project_by_id,
    update_a_project,
    delete_a_project,
)

new_project_name = "happy-test-2022-02-28"


def test_create_a_project():
    response = create_a_project(name=new_project_name)
    assert response is not None


def test_get_a_list_of_projects():
    response = get_a_list_of_projects()
    assert len(response.get("projects")) > 1


def test_get_a_list_of_projects_with_ids():
    response = get_a_list_of_projects(ids=["a2feaa26-a515-4716-a2c5-b39c784980fb",
                                           "98551291-5aa8-4322-95c3-acd5a23c8e65"])
    assert len(response.get("projects")) == 2


def test_get_a_list_of_project_with_names():
    response = get_a_list_of_projects(names=["JS_courselit", "hackyodyssey_courselit_zip"])
    assert len(response.get("projects")) == 2


def test_get_a_list_of_project_with_name():
    response = get_a_list_of_projects(name="jenkins")
    assert len(response.get("projects")) > 1


def test_get_a_list_of_project_with_name_regex():
    response = get_a_list_of_projects(name_regex="(?i)jenkins$")
    assert len(response.get("projects")) == 1


def test_get_project_id_by_name():
    project_id = get_project_id_by_name(name=new_project_name)
    assert project_id is not None


def test_get_all_tags():
    tags = get_all_project_tags()
    assert tags is not None


def test_get_last_scan_info():
    response = get_last_scan_info()
    assert response is not None


def test_get_last_scan_info_filter_by_project_ids():
    response = get_last_scan_info(project_ids=["a2feaa26-a515-4716-a2c5-b39c784980fb",
                                           "98551291-5aa8-4322-95c3-acd5a23c8e65"])
    assert response is not None


def test_get_last_scan_info_filter_by_application_id():
    application_id = "8e339d83-336b-4efe-9989-0fbe8b19d5de"
    response = get_last_scan_info(application_id=application_id)
    assert response is not None


def test_get_branches():
    branches = get_branches()
    assert len(branches) > 1


def test_get_branches_filter_by_project_id():
    branches = get_branches(project_id="a2feaa26-a515-4716-a2c5-b39c784980fb")
    assert len(branches) == 1


def test_get_branches_filter_by_branch_name():
    branches = get_branches(branch_name="demo")
    assert len(branches) > 1


def test_get_a_project_by_id():
    project = get_a_project_by_id(project_id="00592ce6-ee7c-4738-aaff-115d1f864970")
    assert project is not None


def test_update_a_project():
    project_id = '00592ce6-ee7c-4738-aaff-115d1f864970'
    is_successful = update_a_project(
        project_id=project_id,
        repo_url="https://github.com/checkmarx-ts/checkmarx-python-sdk.git"
    )
    assert is_successful is True


def test_delete_a_project():
    project_id = get_project_id_by_name(name=new_project_name)
    if project_id:
        response = delete_a_project(project_id=project_id)
        assert response is True