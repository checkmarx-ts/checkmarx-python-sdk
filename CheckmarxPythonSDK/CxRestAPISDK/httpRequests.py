from .config import config
from CheckmarxPythonSDK.utilities.httpRequests import build_request_funcs, check_response_status_code
from ..__version__ import __version__


def get_headers(api_version="1.0", extra_header=None):
    headers = {
        "cxOrigin": "Checkmarx Python SDK " + __version__,
        "Content-Type": "application/json;v={}".format(api_version),
    }
    if extra_header and isinstance(extra_header, dict):
        headers.update(extra_header)
    return headers


def get_data_from_config():
    server_url = config.get("base_url")
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
    proxies = {
        "http": config.get("proxy"),
        "https": config.get("proxy"),
    }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data, proxies


get, post, put, patch, delete, _, _ = build_request_funcs(get_data_from_config)


def get_request(relative_url, headers=(), is_iam=False):
    response = get(relative_url, headers=headers, is_iam=is_iam)
    check_response_status_code(response)
    return response


def post_request(relative_url, data, files=None, headers=(), is_iam=False):
    response = post(relative_url, data=data, files=files, headers=headers, is_iam=is_iam)
    check_response_status_code(response)
    return response


def put_request(relative_url, data, files=None, headers=(), is_iam=False):
    response = put(relative_url, data=data, files=files, headers=headers, is_iam=is_iam)
    check_response_status_code(response)
    return response


def patch_request(relative_url, data, headers=(), is_iam=False):
    response = patch(relative_url, data=data, headers=headers, is_iam=is_iam)
    check_response_status_code(response)
    return response


def delete_request(relative_url, data=None, headers=(), is_iam=False):
    response = delete(relative_url, data=data, headers=headers, is_iam=is_iam)
    check_response_status_code(response)
    return response
