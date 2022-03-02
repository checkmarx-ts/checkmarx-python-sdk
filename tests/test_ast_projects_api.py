from CheckmarxPythonSDK.CxAST import (
    create_a_project,
    get_a_list_of_projects,
    get_project_id_by_name,
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
    project_id = get_project_id_by_name("AST_Jenkins")
    assert project_id is not None


def test_delete_a_project():
    project_id = get_project_id_by_name(name=new_project_name)
    response = delete_a_project(project_id=project_id)
    assert response is True