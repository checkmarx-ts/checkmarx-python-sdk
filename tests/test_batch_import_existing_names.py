from unittest.mock import MagicMock, call, patch

import httpx
import pytest

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


def test_next_round_starts_immediately_and_polls_back_off():
    api = _api()
    api.get_job_status = MagicMock(side_effect=[None, 50, 100])
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    # polls: None -> sleep 2s, 50 -> sleep 4s, 100 -> no trailing sleep
    assert s.call_args_list == [call(2.0), call(4.0)]
    api.repo_import.assert_called_once()


def test_poll_interval_caps_at_delay_request_timeout():
    api = _api()
    api.get_job_status = MagicMock(side_effect=[None] * 8 + [100])
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        api.batch_import_repo(
            REPOS, "GITLAB", "o", "code", delay_request_timeout=10
        )
    assert [c.args[0] for c in s.call_args_list] == [
        2.0, 4.0, 8.0, 10, 10, 10, 10, 10
    ]


def test_transient_poll_error_does_not_abort_batch():
    api = _api()
    api.get_job_status = MagicMock(
        side_effect=[httpx.RemoteProtocolError("boom"), 100]
    )
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    assert s.call_args_list == [call(2.0)]
    api.repo_import.assert_called_once()


def test_round_raises_timeout_when_job_never_finishes():
    api = _api()
    api.get_job_status = MagicMock(return_value=None)
    clock = [0.0]
    with patch.object(
        m.time, "monotonic", side_effect=lambda: clock[0]
    ), patch.object(
        m.time, "sleep", side_effect=lambda t: clock.__setitem__(0, clock[0] + t)
    ), patch.object(m, "get_all_projects", return_value=[]):
        with pytest.raises(TimeoutError):
            api.batch_import_repo(
                REPOS,
                "GITLAB",
                "o",
                "code",
                delay_request_timeout=10,
                max_wait_per_round=30,
            )
