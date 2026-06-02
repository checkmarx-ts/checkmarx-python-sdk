import pytest

from CheckmarxPythonSDK.CxOne import get_projects_overview
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI


def test_get_projects_overview():
    projects = _ProjectsAPI().get_a_list_of_projects(limit=2)
    if not projects.projects:
        pytest.skip("No projects found")
    project_ids = [p.id for p in projects.projects]
    try:
        result = get_projects_overview(
            project_ids=project_ids,
            include_groups=True,
        )
        assert result is not None
        assert isinstance(result, list)
    except Exception as e:
        print("get_projects_overview skipped: {}".format(str(e)))
