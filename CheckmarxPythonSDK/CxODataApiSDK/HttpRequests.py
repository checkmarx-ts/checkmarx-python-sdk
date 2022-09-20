from CheckmarxPythonSDK.CxRestAPISDK.config import config
from CheckmarxPythonSDK.utilities.httpRequests import build_request_funcs
from ..CxPortalSoapApiSDK import get_version_number_as_int


def get_basic_auth():
    basic_auth = None
    if get_version_number_as_int() < 900:
        from requests.auth import HTTPBasicAuth
        basic_auth = HTTPBasicAuth(config.get("username"), config.get("password"))
    return basic_auth


def get_data_from_config():
    server_url = config.get("base_url")
    token_url = config.get("base_url") + "/cxrestapi/auth/identity/connect/token"
    timeout = config.get("timeout")
    verify_ssl_cert = config.get("verify")
    cert = config.get("cert")
    username = config.get("username")
    password = config.get("password")
    token_req_data = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "access_control_api sast_api",
        "client_id": "resource_owner_sast_client",
        "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C",
    }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data


get, _, _, _, _ = build_request_funcs(get_data_from_config)


def get_value_from_response(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs).json().get("value")
    return inner


def http_get(relative_url):
    return get(relative_url=relative_url, auth=get_basic_auth())


@get_value_from_response
def get_request(relative_url):
    return http_get(relative_url)


def get_request_with_raw_response(relative_url):
    return http_get(relative_url)
