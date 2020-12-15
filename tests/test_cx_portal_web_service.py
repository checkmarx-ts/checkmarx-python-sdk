# encoding: utf-8

from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    add_license_expiration_notification,
    create_new_preset, delete_preset, get_preset_list, get_server_license_data, get_server_license_summary,
    delete_project, delete_projects, get_version_number, get_path_comments_history,
    get_name_of_user_who_marked_false_positive_from_comments_history
)


def test_add_license_expiration_notification():
    response = add_license_expiration_notification()
    assert response.get("IsSuccesfull") is True


def test_create_new_preset():
    response = create_new_preset(query_ids=[343], name="ddd10")
    assert response['IsSuccesfull'] is True


def test_delete_preset():
    response = delete_preset(preset_id=120006)
    assert response["IsSuccesfull"] is True


def test_delete_project():
    response = delete_project(project_id=3)
    assert response["IsSuccesfull"] is True


def test_delete_projects():
    response = delete_projects(project_ids=[8], flag="OnlyAllowedProjects")
    assert response["IsSuccesfull"] is True


def test_get_path_comments_history():
    scan_id = 1000022
    path_id = 5
    label_type = 'Remark'
    response = get_path_comments_history(scan_id=scan_id, path_id=path_id, label_type=label_type)
    assert response.get("IsSuccesfull") is True


def test_get_name_of_user_who_marked_false_positive_from_comments_history():
    scan_id = 1000022
    path_id = 5
    response = get_name_of_user_who_marked_false_positive_from_comments_history(scan_id=scan_id, path_id=path_id)
    assert response is not None


def test_get_preset_list():
    response = get_preset_list()
    assert response["IsSuccesfull"] is True


def test_get_server_license_data():
    lic = get_server_license_data()
    assert lic is not None


def test_get_server_license_summary():
    lic = get_server_license_summary()
    assert lic is not None


def test_get_version_number():
    version = get_version_number()
    assert version is not None
