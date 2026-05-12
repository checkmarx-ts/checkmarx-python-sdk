import pytest
from unittest.mock import MagicMock, patch

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.configuration import Configuration


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _config(max_retries=2):
    return Configuration(
        server_base_url="https://example.com",
        # "iam.checkmarx.net" triggers the client_credentials branch in
        # create_token_request_data, which is the CxOne flow under test.
        token_url="https://iam.checkmarx.net/auth/realms/test/protocol/openid-connect/token",
        client_id="test-client",
        client_secret="test-secret",
        max_retries=max_retries,
        rate_limit_capacity=1000,
        rate_limit_period=60,
    )


def _http_response(status_code, method="GET", text=""):
    """Build a minimal mock httpx response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.headers = {}
    resp.request = MagicMock()
    resp.request.method = method
    return resp


def _token_response(token):
    """Build a mock token-endpoint response."""
    resp = MagicMock()
    resp.json.return_value = {"access_token": token}
    return resp


def _make_client(config, mock_session):
    with patch("CheckmarxPythonSDK.api_client.create_session", return_value=mock_session):
        return ApiClient(configuration=config, url_prefix="")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestTokenExpiry:

    def test_initial_token_is_none_before_first_request(self):
        """Token manager holds no token until the first API call is made."""
        config = _config()
        session = MagicMock()
        client = _make_client(config, session)

        assert client.token_manager.current_token is None

    def test_token_fetched_lazily_on_first_request(self):
        """First request triggers an automatic token fetch via the token endpoint."""
        config = _config()
        session = MagicMock()
        session.post.return_value = _token_response("initial_token")
        session.request.return_value = _http_response(200)

        client = _make_client(config, session)
        client.call_api(method="GET", url="https://example.com/api/resource")

        session.post.assert_called_once()
        assert client.token_manager.current_token == "initial_token"

    def test_no_refresh_on_successful_200(self):
        """A 200 response does not trigger a token refresh."""
        config = _config()
        session = MagicMock()
        session.post.return_value = _token_response("valid_token")
        session.request.return_value = _http_response(200)

        client = _make_client(config, session)
        client.call_api(method="GET", url="https://example.com/api/resource")

        # post called exactly once: the lazy initial fetch, never for a refresh
        assert session.post.call_count == 1
        assert session.request.call_count == 1

    def test_expired_token_triggers_refresh_and_retries(self):
        """On 401 the client refreshes the token and retries — succeeds on the second attempt."""
        config = _config(max_retries=2)
        session = MagicMock()
        session.post.side_effect = [
            _token_response("expired_token"),
            _token_response("refreshed_token"),
        ]
        session.request.side_effect = [
            _http_response(401),   # first attempt: server rejects expired token
            _http_response(200),   # second attempt: succeeds with refreshed token
        ]

        client = _make_client(config, session)
        result = client.call_api(method="GET", url="https://example.com/api/resource")

        assert result.status_code == 200
        # post: once for initial fetch, once for explicit refresh after 401
        assert session.post.call_count == 2
        # request: once with expired token, once with refreshed token
        assert session.request.call_count == 2

    def test_retry_uses_refreshed_token_in_authorization_header(self):
        """The Authorization header on the retry carries the refreshed token, not the expired one."""
        config = _config(max_retries=2)
        session = MagicMock()
        session.post.side_effect = [
            _token_response("expired_token"),
            _token_response("refreshed_token"),
        ]
        session.request.side_effect = [
            _http_response(401),
            _http_response(200),
        ]

        client = _make_client(config, session)
        client.call_api(method="GET", url="https://example.com/api/resource")

        first_headers = session.request.call_args_list[0].kwargs["headers"]
        retry_headers = session.request.call_args_list[1].kwargs["headers"]
        assert first_headers["Authorization"] == "Bearer expired_token"
        assert retry_headers["Authorization"] == "Bearer refreshed_token"

    def test_persistent_401_exhausts_retries_and_raises(self):
        """When the server keeps returning 401 after all retries, raise_for_status() is called."""
        config = _config(max_retries=1)
        session = MagicMock()
        session.post.return_value = _token_response("some_token")

        expired_resp = _http_response(401)
        expired_resp.raise_for_status.side_effect = Exception("401 Unauthorized")
        session.request.return_value = expired_resp

        client = _make_client(config, session)

        with pytest.raises(Exception, match="401 Unauthorized"):
            client.call_api(method="GET", url="https://example.com/api/resource")

        expired_resp.raise_for_status.assert_called_once()
        # max_retries=1 means 2 total attempts (0 + 1 retry)
        assert session.request.call_count == 2

    def test_refresh_token_updates_current_token(self):
        """Calling refresh_token() on the token manager replaces the stored token."""
        config = _config()
        session = MagicMock()
        session.post.side_effect = [
            _token_response("first_token"),
            _token_response("second_token"),
        ]
        session.request.return_value = _http_response(200)

        client = _make_client(config, session)

        # Trigger initial fetch
        client.call_api(method="GET", url="https://example.com/api/resource")
        assert client.token_manager.current_token == "first_token"

        # Explicit refresh replaces the stored token
        client.token_manager.refresh_token()
        assert client.token_manager.current_token == "second_token"
