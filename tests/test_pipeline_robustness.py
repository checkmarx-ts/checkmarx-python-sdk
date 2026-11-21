import httpx
import pytest
from unittest.mock import MagicMock, patch

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.CxOne.reportAPI import ReportAPI
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI


def _config(max_retries=2):
    return Configuration(
        server_base_url="https://example.com",
        token_url="https://iam.checkmarx.net/auth/realms/t/protocol/openid-connect/token",
        client_id="c",
        client_secret="s",
        timeout=10,
        max_retries=max_retries,
        rate_limit_capacity=1000,
        rate_limit_period=60,
    )


def _ok(method="GET"):
    r = MagicMock()
    r.status_code = 200
    r.headers = {}
    r.request.method = method
    return r


def _client(session, max_retries=2):
    token = MagicMock()
    token.json.return_value = {"access_token": "t"}
    session.post.return_value = token
    with patch("CheckmarxPythonSDK.api_client.create_session", return_value=session):
        return ApiClient(configuration=_config(max_retries))


@pytest.fixture(autouse=True)
def no_sleep():
    with patch("time.sleep"):
        yield


def test_call_api_uses_configured_timeout_by_default():
    session = MagicMock()
    session.request.return_value = _ok()
    _client(session).call_api("GET", "https://example.com/x")
    assert session.request.call_args.kwargs["timeout"] == 10


def test_call_api_per_call_timeout_overrides_configured():
    session = MagicMock()
    session.request.return_value = _ok()
    _client(session).call_api("GET", "https://example.com/x", timeout=900)
    assert session.request.call_args.kwargs["timeout"] == 900


def test_get_retries_after_read_timeout():
    session = MagicMock()
    session.request.side_effect = [httpx.ReadTimeout("slow"), _ok()]
    resp = _client(session).call_api("GET", "https://example.com/x")
    assert resp.status_code == 200
    assert session.request.call_count == 2


def test_get_raises_after_retries_exhausted():
    session = MagicMock()
    session.request.side_effect = httpx.ReadTimeout("slow")
    with pytest.raises(httpx.ReadTimeout):
        _client(session, max_retries=2).call_api("GET", "https://example.com/x")
    assert session.request.call_count == 3


def test_post_is_not_retried_after_timeout():
    session = MagicMock()
    session.request.side_effect = httpx.ReadTimeout("slow")
    with pytest.raises(httpx.ReadTimeout):
        _client(session).call_api("POST", "https://example.com/x")
    assert session.request.call_count == 1


def _report_api(statuses, key="status"):
    api_client = MagicMock()
    api_client.configuration.server_base_url = "https://example.com"
    responses = []
    for st in statuses:
        r = MagicMock()
        r.json.return_value = {key: st, "reportId": "rid", "exportId": "eid"}
        responses.append(r)
    api_client.call_api.side_effect = responses + [responses[-1]] * 1000
    return ReportAPI(api_client=api_client)


def test_report_generation_failure_raises_instead_of_looping():
    api = _report_api(["processing", "failed"])
    with pytest.raises(RuntimeError, match="failed"):
        api.create_scan_report("pdf", "scan", "proj")


def test_report_generation_times_out():
    api = _report_api(["processing"])
    with pytest.raises(TimeoutError):
        api.create_scan_report("pdf", "scan", "proj", max_wait=0)


def test_sca_export_failure_raises():
    api = _report_api(["Failed"], key="exportStatus")
    with pytest.raises(RuntimeError, match="failed"):
        api.get_sca_scan_report("eid")


def test_sca_export_times_out():
    api = _report_api(["Pending"], key="exportStatus")
    with pytest.raises(TimeoutError):
        api.get_sca_scan_report("eid", max_wait=0)


def test_get_all_projects_propagates_errors():
    api = ProjectsAPI(api_client=MagicMock())
    with patch.object(ProjectsAPI, "get_a_list_of_projects", side_effect=httpx.ReadTimeout("x")):
        with pytest.raises(httpx.ReadTimeout):
            api.get_all_projects()
