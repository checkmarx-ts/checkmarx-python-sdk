from unittest.mock import patch

from CheckmarxPythonSDK import api_client
from CheckmarxPythonSDK.configuration import Configuration


def test_create_session_applies_timeout():
    # the session default timeout also covers the suds SOAP transport
    cfg = Configuration(server_base_url="http://x", verify=False, timeout=123)
    session = api_client.create_session(cfg)
    assert session.timeout.read == 123
    assert session.timeout.connect == 123


def test_create_session_applies_proxy_and_cert():
    cfg = Configuration(server_base_url="http://x", verify=False,
                        cert="client.pem", proxy="http://proxy:8080")
    with patch.object(api_client.httpx, "HTTPTransport") as ht, \
            patch.object(api_client.httpx, "Client"):
        api_client.create_session(cfg)
    kwargs = ht.call_args.kwargs
    assert kwargs["proxy"] == "http://proxy:8080"
    assert kwargs["cert"] == "client.pem"
