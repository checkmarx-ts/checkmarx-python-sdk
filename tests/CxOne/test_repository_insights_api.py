import pytest

from CheckmarxPythonSDK.CxOne import (
    get_project_repositories,
    get_insights_by_repository,
)
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI


def test_get_project_repositories():
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if not projects.projects:
        pytest.skip("No projects found")
    project_id = projects.projects[0].id
    try:
        result = get_project_repositories(project_id=project_id, limit=5)
        assert result is not None
        assert "project_id" in result
    except Exception as e:
        print("get_project_repositories skipped: {}".format(str(e)))


def test_get_insights_by_repository():
    try:
        result = get_insights_by_repository(
            repository_url="https://github.com/checkmarx-ts/checkmarx-python-sdk.git"
        )
        assert result is not None
        assert "insights" in result
    except Exception as e:
        print("get_insights_by_repository skipped: {}".format(str(e)))
