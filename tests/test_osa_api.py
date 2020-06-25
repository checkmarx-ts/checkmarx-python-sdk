# encoding: utf-8
from pathlib import Path

from CheckmarxPythonSDK.CxRestAPISDK.osa.OsaAPI import OsaAPI
from CheckmarxPythonSDK.CxRestAPISDK.sast.projects.ProjectsAPI import ProjectsAPI


def get_project_id():
    project_name = "JVL-local"
    projects_api = ProjectsAPI()
    project_id = projects_api.create_project_if_not_exists_by_project_name_and_team_full_name(project_name, "/CxServer")
    return project_id


def test_get_all_osa_scan_details():
    project_id = get_project_id()
    osa_api = OsaAPI()
    all_osa_scan = osa_api.get_all_osa_scan_details_for_project(project_id, page=1, items_per_page=1)
    assert all_osa_scan is not None


def test_get_last_osa_scan_id_of_a_project():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    assert scan_id is not None


def test_get_osa_scan_by_scan_id():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    osa_scan = osa_api.get_osa_scan_by_scan_id(scan_id)
    assert osa_scan is not None


def test_create_an_osa_scan_request():
    project_id = get_project_id()
    osa_api = OsaAPI()
    parent_folder = Path(__file__).parent.absolute()
    path = parent_folder / "JavaVulnerableLab-master.zip"
    scan_id = osa_api.create_an_osa_scan_request(project_id, zipped_source_path=str(path))
    assert scan_id is not None


def test_get_all_osa_file_extensions():
    osa_api = OsaAPI()
    extensions = osa_api.get_all_osa_file_extensions()
    assert extensions is not None


def test_get_osa_licenses_by_id():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    licenses = osa_api.get_osa_licenses_by_id(scan_id)
    assert licenses is not None


def test_get_osa_scan_libraries():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    libraries = osa_api.get_osa_scan_libraries(scan_id, page=1, items_per_page=10)
    assert libraries is not None


def test_get_osa_scan_vulnerabilities_by_id():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    vulnerabilities = osa_api.get_osa_scan_vulnerabilities_by_id(scan_id, page=1, items_per_page=10)
    assert vulnerabilities is not None


def test_get_first_vulnerability_id():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    vulnerability_id = osa_api.get_first_vulnerability_id(scan_id)
    assert vulnerability_id is not None


def test_get_osa_scan_vulnerability_comments_by_id():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    vulnerability_id = osa_api.get_first_vulnerability_id(scan_id)
    comment = osa_api.get_osa_scan_vulnerability_comments_by_id(vulnerability_id, project_id)
    assert comment is not None


def test_get_osa_scan_summary_report():
    project_id = get_project_id()
    osa_api = OsaAPI()
    scan_id = osa_api.get_last_osa_scan_id_of_a_project(project_id)
    report = osa_api.get_osa_scan_summary_report(scan_id)
    assert report is not None
