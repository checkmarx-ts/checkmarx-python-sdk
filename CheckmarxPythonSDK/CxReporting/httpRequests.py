from .config import config
from CheckmarxPythonSDK.utilities.httpRequests import build_request_funcs


def get_data_from_config():
    server_url = config.get("reporting_client_url")
    token_url = config.get("base_url") + "/cxrestapi/auth/identity/connect/token"
    timeout = config.get("timeout")
    verify_ssl_cert = config.get("verify")
    cert = config.get("cert")
    username = config.get("username")
    password = config.get("password")
    grant_type = config.get("grant_type")
    scope = config.get("scope")
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")

    token_req_data = {
        "username": username,
        "password": password,
        "grant_type": grant_type,
        "scope": scope,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data


get_request, post_request, _, _, _ = build_request_funcs(get_data_from_config)
