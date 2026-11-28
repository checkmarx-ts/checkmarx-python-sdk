from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne import get_scm_types  # noqa: F401
from CheckmarxPythonSDK.CxOne.repoManagerAPI import (
    RepoManagerAPI,
    ScmTypeInfo,
)


def _api(payload=None, text=""):
    client = MagicMock()
    client.configuration.server_base_url = "https://example.com"
    resp = client.call_api.return_value
    resp.json.return_value = payload
    resp.text = text
    return RepoManagerAPI(api_client=client), client


def test_get_scm_types_request_and_parsing():
    api, client = _api([
        {"id": 1, "name": "github", "displayName": "GitHub", "scope": "repo", "future": 1},
        {"id": 2, "name": "gitlab", "displayName": "GitLab", "scope": "api"},
    ])
    types = api.get_scm_types()
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["method"] == "GET"
    assert kwargs["url"] == "https://example.com/api/repos-manager/scm-types"
    assert [t.id for t in types] == [1, 2]
    assert isinstance(types[1], ScmTypeInfo)
    assert (types[1].name, types[1].displayName, types[1].scope) == ("gitlab", "GitLab", "api")


def test_job_status_returns_last_percentage_ignoring_noise():
    body = (
        ": keep-alive\n\n"
        "event: progress\n"
        'data: {"percentage": 10}\n\n'
        "data: not json\n\n"
        'data: {"other": 1}\n\n'
        'data: {"percentage": 100}\n\n'
    )
    api, client = _api(text=body)
    assert api.get_job_status() == 100
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["url"] == "https://example.com/api/ssegateway/job-status"
    assert kwargs["headers"] == {"accept": "*/*", "Accept-Encoding": "identity"}


def test_job_status_none_for_empty_or_eventless_stream():
    assert _api(text="")[0].get_job_status() is None
    assert _api(text=": ping\n\n")[0].get_job_status() is None
    assert _api(text='data: {"percentage": 0}\n')[0].get_job_status() == 0


def test_job_status_details_parses_full_event():
    body = (
        'data: {"currentPhase":"DONE","percentage":100.0,'
        '"jobRunning":false}\n\n'
        'data: {"currentPhase":"RUNNING","percentage":42.0,'
        '"jobRunning":true}\n\n'
    )
    api, client = _api(text=body)
    status = api.get_job_status_details()
    assert status.percentage == 42.0
    assert status.job_running is True
    assert status.current_phase == "RUNNING"
    # get_job_status keeps returning the plain percentage
    assert api.get_job_status() == 42.0
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["url"] == "https://example.com/api/ssegateway/job-status"
    assert kwargs["headers"] == {"accept": "*/*", "Accept-Encoding": "identity"}


def test_job_status_details_none_for_empty_stream():
    assert _api(text="")[0].get_job_status_details() is None
    assert _api(text=": ping\n\n")[0].get_job_status_details() is None
