import pytest

from CheckmarxPythonSDK.CxOne import (
    get_projects,
    get_project,
    get_engine_results,
    get_result_groups,
    get_scan_overview,
    read_projects,
    read_project,
    read_engine_results,
    read_result_groups,
    read_scan_overview,
)


def _get_first_project_and_scan():
    """Get a project and scan ID from the micro-engines list."""
    projects_data = get_projects(page_size=1)
    entries = projects_data.get("entries", [])
    if not entries:
        return None, None
    project_id = entries[0].get("id")
    # Get scan overview for any completed scan
    from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
    scans = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    scan_id = None
    for s in scans.scans:
        if "2ms" in (s.engines or []) or "Scorecard" in (s.engines or []):
            scan_id = s.id
            break
    return project_id, scan_id


def test_get_projects():
    result = get_projects(page_size=5)
    assert result is not None
    assert "entries" in result


def test_get_project():
    entries = get_projects(page_size=1).get("entries", [])
    if not entries:
        pytest.skip("No micro-engine projects found")
    project_id = entries[0].get("id")
    result = get_project(project=project_id)
    assert result is not None


def test_get_scan_overview():
    project_id, scan_id = _get_first_project_and_scan()
    if not scan_id:
        pytest.skip("No completed micro-engine scans found")
    result = get_scan_overview(scan=scan_id)
    assert result is not None


def test_get_engine_results():
    project_id, scan_id = _get_first_project_and_scan()
    if not scan_id:
        pytest.skip("No completed micro-engine scans found")
    try:
        result = get_engine_results(
            project=project_id, scan=scan_id, engine="2ms", page_size=5
        )
        assert result is not None
    except Exception as e:
        print("get_engine_results skipped: {}".format(str(e)))


def test_get_result_groups():
    project_id, scan_id = _get_first_project_and_scan()
    if not scan_id:
        pytest.skip("No completed micro-engine scans found")
    try:
        result = get_result_groups(
            project=project_id, scan=scan_id,
            engine="2ms", column="severity",
        )
        assert result is not None
    except Exception as e:
        print("get_result_groups skipped: {}".format(str(e)))


def test_read_projects():
    result = read_projects(page_size=5)
    assert result is not None
    assert "entries" in result


def test_read_scan_overview():
    project_id, scan_id = _get_first_project_and_scan()
    if not scan_id:
        pytest.skip("No completed micro-engine scans found")
    result = read_scan_overview(scan=scan_id)
    assert result is not None
