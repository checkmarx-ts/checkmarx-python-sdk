from unittest.mock import MagicMock, patch

from CheckmarxPythonSDK.CxOne import projectsAPI as m
from CheckmarxPythonSDK.CxOne import repoManagerAPI as rm


def _proj(name, pid):
    p = MagicMock()
    p.name = name
    p.id = pid
    return p


def test_delete_projects_by_pattern_filters_and_collects_failures():
    api = m.ProjectsAPI.__new__(m.ProjectsAPI)
    api.get_all_projects = MagicMock(
        return_value=[_proj("org/a", "1"), _proj("org/b", "2"), _proj("other/c", "3")]
    )
    api.delete_a_project = MagicMock(side_effect=[True, False, True])
    failed = api.delete_projects_by_pattern("org/*")
    assert failed == ["org/b"]
    # non-matching project never attempted
    deleted_ids = [c.kwargs["project_id"] for c in api.delete_a_project.call_args_list]
    assert deleted_ids == ["1", "2"]


def test_delete_projects_by_pattern_parallel_workers():
    api = m.ProjectsAPI.__new__(m.ProjectsAPI)
    api.get_all_projects = MagicMock(return_value=[_proj(f"org/{i}", str(i)) for i in range(20)])
    api.delete_a_project = MagicMock(
        side_effect=[True] * 18 + [False, Exception("boom")]
    )
    failed = api.delete_projects_by_pattern("org/*", workers=4)
    assert len(failed) == 2
    # worker completion order is nondeterministic; one plain failure, one exception
    plain = [f for f in failed if "Exception" not in f]
    errored = [f for f in failed if "Exception" in f]
    assert len(plain) == 1 and len(errored) == 1


def test_no_match_returns_empty_without_deleting():
    api = m.ProjectsAPI.__new__(m.ProjectsAPI)
    api.get_all_projects = MagicMock(return_value=[_proj("org/a", "1")])
    api.delete_a_project = MagicMock()
    assert api.delete_projects_by_pattern("nothing/*") == []
    api.delete_a_project.assert_not_called()


def test_module_level_functions_reuse_one_projects_api():
    with patch.object(m, "ProjectsAPI") as factory:
        old = m._projects_api
        m._projects_api = m.LazySingleton(factory)
        try:
            m.get_all_projects()
            m.delete_a_project(project_id="1")
        finally:
            m._projects_api = old
    assert factory.call_count == 1


def test_module_level_functions_reuse_one_repo_manager_api():
    with patch.object(rm, "RepoManagerAPI") as factory:
        old = rm._repo_manager_api
        rm._repo_manager_api = rm.LazySingleton(factory)
        try:
            rm.check_origin(origin="GITLAB")
            rm.get_job_status()
        finally:
            rm._repo_manager_api = old
    assert factory.call_count == 1
