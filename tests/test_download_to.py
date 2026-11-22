import os

import httpx
import pytest
from unittest.mock import MagicMock, patch

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.configuration import Configuration


def _client(handler, max_retries=2):
    cfg = Configuration(
        server_base_url="https://example.com",
        token_url="https://iam.checkmarx.net/auth/realms/t/protocol/openid-connect/token",
        client_id="c", client_secret="s", timeout=10, max_retries=max_retries,
        rate_limit_capacity=1000, rate_limit_period=60,
    )
    session = httpx.Client(transport=httpx.MockTransport(handler))
    with patch("CheckmarxPythonSDK.api_client.create_session", return_value=session):
        client = ApiClient(configuration=cfg)
    client.token_manager.current_token = "tok"
    client.token_manager.token_refresh_func = lambda: "tok2"
    return client


@pytest.fixture(autouse=True)
def no_sleep():
    with patch("time.sleep"):
        yield


def test_streams_body_to_file_and_sends_auth(tmp_path):
    seen = {}

    def handler(request):
        seen["auth"] = request.headers["Authorization"]
        return httpx.Response(200, content=b"x" * 5000)

    dest = tmp_path / "r.bin"
    out = _client(handler).download_to("GET", "https://example.com/r", str(dest), chunk_size=1000)
    assert out == str(dest)
    assert dest.read_bytes() == b"x" * 5000
    assert seen["auth"] == "Bearer tok"
    assert not os.path.exists(f"{dest}.part")


def test_http_error_raises_and_leaves_no_file(tmp_path):
    dest = tmp_path / "r.bin"
    client = _client(lambda r: httpx.Response(404, text="nope"))
    with pytest.raises(ValueError, match="404"):
        client.download_to("GET", "https://example.com/r", str(dest))
    assert not dest.exists() and not os.path.exists(f"{dest}.part")


def test_401_refreshes_token_once(tmp_path):
    calls = []

    def handler(request):
        calls.append(request.headers["Authorization"])
        if len(calls) == 1:
            return httpx.Response(401)
        return httpx.Response(200, content=b"ok")

    dest = tmp_path / "r.bin"
    _client(handler).download_to("GET", "https://example.com/r", str(dest))
    assert calls == ["Bearer tok", "Bearer tok2"]
    assert dest.read_bytes() == b"ok"


def test_get_retries_on_timeout_and_restarts_download(tmp_path):
    attempts = []

    def handler(request):
        attempts.append(1)
        if len(attempts) == 1:
            raise httpx.ReadTimeout("slow", request=request)
        return httpx.Response(200, content=b"full")

    dest = tmp_path / "r.bin"
    _client(handler).download_to("GET", "https://example.com/r", str(dest))
    assert len(attempts) == 2 and dest.read_bytes() == b"full"


def test_post_not_retried_on_timeout(tmp_path):
    attempts = []

    def handler(request):
        attempts.append(1)
        raise httpx.ReadTimeout("slow", request=request)

    dest = tmp_path / "r.bin"
    with pytest.raises(httpx.ReadTimeout):
        _client(handler).download_to("POST", "https://example.com/r", str(dest))
    assert len(attempts) == 1 and not dest.exists()


def test_midstream_failure_keeps_existing_file_intact(tmp_path):
    dest = tmp_path / "r.bin"
    dest.write_bytes(b"old")

    class Boom(httpx.SyncByteStream):
        def __iter__(self):
            yield b"partial"
            raise httpx.ReadError("dropped")

    client = _client(lambda r: httpx.Response(200, stream=Boom()), max_retries=0)
    with pytest.raises(httpx.ReadError):
        client.download_to("GET", "https://example.com/r", str(dest))
    assert dest.read_bytes() == b"old"
    assert not os.path.exists(f"{dest}.part")


def test_per_call_timeout_is_passed_to_httpx(tmp_path):
    seen = {}

    def handler(request):
        seen["timeout"] = request.extensions["timeout"]
        return httpx.Response(200, content=b"")

    _client(handler).download_to("GET", "https://example.com/r", str(tmp_path / "a"), timeout=900)
    assert seen["timeout"]["read"] == 900


def test_download_sca_scan_report_waits_then_streams(tmp_path):
    from CheckmarxPythonSDK.CxOne.reportAPI import ReportAPI

    api_client = MagicMock()
    api_client.configuration.server_base_url = "https://example.com"
    pending, done = MagicMock(), MagicMock()
    pending.json.return_value = {"exportStatus": "Pending"}
    done.json.return_value = {"exportStatus": "Completed"}
    api_client.call_api.side_effect = [pending, done]
    api_client.download_to.return_value = "out.json"

    result = ReportAPI(api_client=api_client).download_sca_scan_report("eid", "out.json", timeout=900)

    assert result == "out.json"
    args, kwargs = api_client.download_to.call_args
    assert args == ("GET", "https://example.com/api/sca/export/requests/eid/download", "out.json")
    assert kwargs["timeout"] == 900
