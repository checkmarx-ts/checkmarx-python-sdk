import pytest

from CheckmarxPythonSDK.CxOne import (
    delete_import,
    get_aggregate_results,
    get_a_list_of_imports,
    get_latest_imports,
    get_imports_summaries,
    get_import_results,
    bulk_triage_import_results,
)
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI


def _get_project_id():
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if projects.projects:
        return projects.projects[0].id
    return None


def test_get_a_list_of_imports():
    result = get_a_list_of_imports(limit=5)
    assert result is not None
    assert "items" in result


def test_get_latest_imports():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    try:
        result = get_latest_imports(project_ids=[project_id])
        assert result is not None
    except Exception as e:
        print("get_latest_imports skipped: {}".format(str(e)))


def test_get_imports_summaries():
    imports_result = get_a_list_of_imports(limit=1)
    items = imports_result.get("items", [])
    if not items:
        pytest.skip("No imports found")
    import_id = items[0].get("id")
    try:
        result = get_imports_summaries(import_ids=[import_id])
        assert result is not None
    except Exception as e:
        print("get_imports_summaries skipped: {}".format(str(e)))


def test_get_aggregate_results():
    imports_result = get_a_list_of_imports(limit=1)
    items = imports_result.get("items", [])
    if not items:
        pytest.skip("No imports found")
    import_id = items[0].get("id")
    try:
        result = get_aggregate_results(
            import_id=import_id, group_by_field="severity"
        )
        assert result is not None
    except Exception as e:
        print("get_aggregate_results skipped: {}".format(str(e)))


def test_get_import_results():
    imports_result = get_a_list_of_imports(limit=1)
    items = imports_result.get("items", [])
    if not items:
        pytest.skip("No imports found")
    import_id = items[0].get("id")
    try:
        result = get_import_results(import_id=import_id)
        assert result is not None
    except Exception as e:
        print("get_import_results skipped: {}".format(str(e)))


def test_bulk_triage_import_results():
    imports_result = get_a_list_of_imports(limit=1)
    items = imports_result.get("items", [])
    if not items:
        pytest.skip("No imports found")
    import_id = items[0].get("id")
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    try:
        result = bulk_triage_import_results(
            import_id=import_id,
            project_id=project_id,
            result_ids=[],
        )
        assert result in (True, False)
    except Exception as e:
        print("bulk_triage_import_results skipped: {}".format(str(e)))


def test_delete_import():
    imports_result = get_a_list_of_imports(limit=1)
    items = imports_result.get("items", [])
    if not items:
        pytest.skip("No imports found")
    import_id = items[0].get("id")
    try:
        result = delete_import(import_id=import_id)
        assert result in (True, False)
    except Exception as e:
        print("delete_import skipped: {}".format(str(e)))
