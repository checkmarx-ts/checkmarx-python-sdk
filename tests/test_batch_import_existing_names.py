from unittest.mock import MagicMock, patch

from CheckmarxPythonSDK.CxOne import repoManagerAPI as m

REPOS = [
    {"fullName": "o/a", "url": "u/a", "id": "1", "defaultBranch": "main"},
    {"fullName": "o/b", "url": "u/b", "id": "2", "defaultBranch": "main"},
]


def _api():
    api = m.RepoManagerAPI.__new__(m.RepoManagerAPI)
    api.check_origin = lambda o: o
    api.construct_repo_request = lambda **kw: {"url": kw["http_repo_url"]}
    api.repo_import = MagicMock()
    api.get_job_status = MagicMock(return_value=100)
    return api


def _run(api, **kw):
    with patch.object(m.time, "sleep"):
        api.batch_import_repo(REPOS, "GITLAB", "o", "code", **kw)


def test_existing_names_skips_without_listing_projects():
    api = _api()
    with patch.object(m, "get_all_projects") as g:
        _run(api, existing_project_names=["o/a"])
    g.assert_not_called()
    sent = api.repo_import.call_args.kwargs["repos_from_request"]
    assert [r["url"] for r in sent] == ["u/b"]


def test_default_lists_projects_once():
    api = _api()
    proj = MagicMock()
    proj.name = "o/a"
    with patch.object(m, "get_all_projects", return_value=[proj]) as g:
        _run(api)
    g.assert_called_once()
    assert api.repo_import.call_count == 1


def test_all_skipped_makes_no_import_call():
    api = _api()
    _run(api, existing_project_names={"o/a", "o/b"})
    api.repo_import.assert_not_called()
