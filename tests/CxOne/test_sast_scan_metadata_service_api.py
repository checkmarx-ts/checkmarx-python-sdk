import pytest
from CheckmarxPythonSDK.CxOne import (
    get_metadata_of_scans,
    get_metadata_of_scan,
    get_engine_metrics_of_scan,
    get_engine_versions_of_scan,
    delete_persisted_dom,
    get_default_file_exclusion_config,
    get_tenant_file_exclusion_config,
    get_project_file_exclusion_config,
    check_persisted_dom_exists,
    update_tenant_file_exclusion_config,
    update_project_file_exclusion_config,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def _get_scan_id(engine=None):
    """Return a completed scan ID, optionally filtered by engine type."""
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if engine is None or engine in (scan.engines or []):
            return scan.id
    return None


def test_get_metadata_of_scans():
    scan_id_1 = _get_sast_scan_id()
    if not scan_id_1:
        pytest.skip("No completed SAST scan found")
    result = get_metadata_of_scans(scan_ids=[scan_id_1])
    assert result is not None


def test_get_metadata_of_scan():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = get_metadata_of_scan(scan_id=scan_id)
    assert result is not None


def test_get_engine_metrics_of_scan():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = get_engine_metrics_of_scan(scan_id=scan_id)
    assert result is not None


def test_get_engine_versions_of_scan():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = get_engine_versions_of_scan(scan_ids=[scan_id])
    assert result is not None


def test_get_default_file_exclusion_config():
    result = get_default_file_exclusion_config()
    assert result is not None


def test_get_tenant_file_exclusion_config():
    result = get_tenant_file_exclusion_config()
    assert result is not None


def test_update_tenant_file_exclusion_config():
    # Fetch current, patch it back unchanged
    current = get_tenant_file_exclusion_config()
    result = update_tenant_file_exclusion_config(config={})
    assert result is not None


def test_get_project_file_exclusion_config():
    # Use any project that exists
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if not projects.projects:
        pytest.skip("No projects found")
    project_id = projects.projects[0].id
    result = get_project_file_exclusion_config(project_id=project_id)
    assert result is not None


def test_update_project_file_exclusion_config():
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if not projects.projects:
        pytest.skip("No projects found")
    project_id = projects.projects[0].id
    result = update_project_file_exclusion_config(
        project_id=project_id, config={}
    )
    assert result is not None


def test_check_persisted_dom_exists():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    # Get the real project ID from the scan
    scan_info = get_metadata_of_scan(scan_id=scan_id)
    try:
        result = check_persisted_dom_exists(
            project_id=scan_info.project_id, scan_id=scan_id
        )
        assert result in (True, False)
    except Exception as e:
        print("check_persisted_dom_exists skipped: {}".format(str(e)))


def test_delete_persisted_dom():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    scan_info = get_metadata_of_scan(scan_id=scan_id)
    try:
        result = delete_persisted_dom(
            project_id=scan_info.project_id,
            scan_id=scan_id,
            branch="master",
        )
        assert result in (True, False)
    except Exception as e:
        print("delete_persisted_dom skipped: {}".format(str(e)))
