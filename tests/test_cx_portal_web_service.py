# encoding: utf-8

from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    add_license_expiration_notification,
    create_new_preset, create_scan_report,
    delete_preset, get_preset_list, get_server_license_data, get_server_license_summary,
    delete_project, delete_projects, get_version_number, get_path_comments_history,
    get_queries_categories,
    get_name_of_user_who_marked_false_positive_from_comments_history
)


def test_add_license_expiration_notification():
    response = add_license_expiration_notification()
    assert response.get("IsSuccesfull") is True


def test_create_new_preset():
    response = create_new_preset(query_ids=[343], name="ddd10")
    assert response['IsSuccesfull'] is True


def test_create_scan_report():
    response = create_scan_report(scan_id=1010002, report_type='PDF', display_categories_all=False,
                                  display_categories_ids=list(range(30, 62)))
    assert response["IsSuccesfull"] is True
    assert response["Id"] > 0


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


def test_get_queries_categories():
    response = get_queries_categories()
    assert len(response["QueriesCategories"]) > 1


def test_get_name_of_user_who_marked_false_positive_from_comments_history():
    scan_id = 1010002
    path_id = 1
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
