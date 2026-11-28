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
    api.get_job_status_details = MagicMock(
        side_effect=[
            m.JobStatus(percentage=10.0, job_running=True),
            m.JobStatus(percentage=100.0, job_running=False),
        ]
    )
    return api


def _run(api, **kw):
    kw.setdefault("settle_timeout", 0)
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
    api.get_job_status_details = MagicMock(
        side_effect=[
            m.JobStatus(),  # no event yet
            m.JobStatus(percentage=50.0, job_running=True),
            m.JobStatus(percentage=100.0, job_running=False),
        ]
    )
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    # polls: None -> sleep 2s, 50 -> sleep 4s, 100 -> no trailing sleep
    assert s.call_args_list == [call(2.0), call(4.0)]
    api.repo_import.assert_called_once()


def test_poll_interval_caps_at_delay_request_timeout():
    api = _api()
    api.get_job_status_details = MagicMock(
        side_effect=[
            m.JobStatus(percentage=p, job_running=True)
            for p in (10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0)
        ]
        + [m.JobStatus(percentage=100.0, job_running=False)]
    )
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
    api.get_job_status_details = MagicMock(
        side_effect=[
            httpx.RemoteProtocolError("boom"),
            m.JobStatus(percentage=10.0, job_running=True),
            m.JobStatus(percentage=100.0, job_running=False),
        ]
    )
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    assert s.call_args_list == [call(2.0), call(4.0)]
    api.repo_import.assert_called_once()


def test_round_raises_timeout_when_job_never_finishes():
    api = _api()
    api.get_job_status_details = MagicMock(
        return_value=m.JobStatus(percentage=10.0, job_running=True)
    )
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


def test_stale_100_from_previous_job_does_not_end_round():
    api = _api()
    api.get_job_status_details = MagicMock(
        side_effect=[
            m.JobStatus(percentage=100.0, job_running=False),  # stale replay
            m.JobStatus(percentage=100.0, job_running=False),  # still stale
            m.JobStatus(percentage=50.0, job_running=True),  # new job visible
            m.JobStatus(percentage=100.0, job_running=False),  # new job done
        ]
    )
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    # the stale 100s must not end the round; it ends on the real 100
    assert s.call_args_list == [call(2.0), call(4.0), call(8.0)]
    api.repo_import.assert_called_once()


def test_stale_100_alone_is_accepted_after_settle_timeout():
    api = _api()
    api.get_job_status_details = MagicMock(
        return_value=m.JobStatus(percentage=100.0, job_running=False)
    )
    clock = [0.0]
    sleeps = []
    with patch.object(
        m.time, "monotonic", side_effect=lambda: clock[0]
    ), patch.object(
        m.time,
        "sleep",
        side_effect=lambda t: (clock.__setitem__(0, clock[0] + t),
                               sleeps.append(t)),
    ), patch.object(m, "get_all_projects", return_value=[]):
        api.batch_import_repo(
            REPOS,
            "GITLAB",
            "o",
            "code",
            delay_request_timeout=10,
            settle_timeout=10,
        )
    # job never observed: the unconfirmed 100 is accepted after 10s
    assert sleeps == [2.0, 4.0, 8.0]
    api.repo_import.assert_called_once()


def test_sync_response_skips_polling_and_returns_results():
    api = _api()
    body = {
        "orgConfigResult": {"status": "SUCCESS"},
        "repoConfigResultList": [
            {"name": "o/a", "status": "SUCCESS", "projectId": "p1"},
            {"name": "o/b", "status": "GENERAL_ERROR",
             "statusMessageError": "already imported and was ignored"},
        ],
    }
    resp = MagicMock()
    resp.json.return_value = body
    api.repo_import = MagicMock(return_value=resp)
    with patch.object(m.time, "sleep") as s, patch.object(
        m, "get_all_projects", return_value=[]
    ):
        results = api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    api.get_job_status_details.assert_not_called()
    s.assert_not_called()
    assert results == body["repoConfigResultList"]


def test_non_json_response_falls_back_to_polling():
    api = _api()
    resp = MagicMock()
    resp.json.side_effect = ValueError("not json")
    api.repo_import = MagicMock(return_value=resp)
    with patch.object(m.time, "sleep"), patch.object(
        m, "get_all_projects", return_value=[]
    ):
        results = api.batch_import_repo(REPOS, "GITLAB", "o", "code")
    api.get_job_status_details.assert_called()
    assert results is None
