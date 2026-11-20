from unittest.mock import MagicMock

from suds.transport import Request

from CheckmarxPythonSDK.CxPortalSoapApiSDK.sudsClient import _RequestsTransport


def _response():
    r = MagicMock()
    r.status_code = 200
    r.headers = {}
    r.content = b"<x/>"
    return r


def test_send_passes_configured_timeout():
    session = MagicMock()
    session.post.return_value = _response()
    transport = _RequestsTransport(session, timeout=123)
    transport.send(Request("http://x/y", b"<m/>"))
    assert session.post.call_args.kwargs["timeout"] == 123


def test_open_passes_configured_timeout():
    session = MagicMock()
    session.get.return_value = _response()
    transport = _RequestsTransport(session, timeout=123)
    transport.open(Request("http://x/y?wsdl"))
    assert session.get.call_args.kwargs["timeout"] == 123


def test_create_session_applies_proxy_and_cert(monkeypatch):
    from unittest.mock import patch
    from CheckmarxPythonSDK import api_client
    from CheckmarxPythonSDK.configuration import Configuration

    cfg = Configuration(server_base_url="http://x", verify=False,
                        cert="client.pem", proxy="http://proxy:8080")
    with patch.object(api_client.httpx, "HTTPTransport") as ht, \
            patch.object(api_client.httpx, "Client"):
        api_client.create_session(cfg)
    kwargs = ht.call_args.kwargs
    assert kwargs["proxy"] == "http://proxy:8080"
    assert kwargs["cert"] == "client.pem"
