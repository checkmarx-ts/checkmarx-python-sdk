from .config import config
from CheckmarxPythonSDK.utilities.httpRequests import build_request_funcs, check_response


def get_data_from_config():
    server_url = config.get("server")
    token_url = config.get("access_control_url") + "/identity/connect/token"
    timeout = config.get("timeout")
    verify_ssl_cert = config.get("verify")
    cert = config.get("cert")
    username = config.get("username")
    password = config.get("password")
    account = config.get("account")
    scope = config.get("scope")
    token_req_data = {
        "username": username,
        "password": password,
        "acr_values": "Tenant:" + str(account),
        "grant_type": "password",
        "scope": scope,
        "client_id": "sca_resource_owner",
    }
    proxies = {
        "http": config.get("proxy"),
        "https": config.get("proxy"),
    }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data, proxies


get, post, put, _, delete, _ = build_request_funcs(get_data_from_config)

agent_headers = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/106.0.0.0 Safari/537.36",
}


def get_request(relative_url, params=None, headers=None, is_iam=False):
    temp_headers = agent_headers.copy()
    if headers:
        temp_headers.update(headers)
    response = get(relative_url, params=params, headers=temp_headers, is_iam=is_iam)
    check_response(response)
    return response


def post_request(relative_url, data, params=None, files=None, headers=None, is_iam=False):
    temp_headers = agent_headers.copy()
    if headers:
        temp_headers.update(headers)
    response = post(relative_url, data, params=params, files=files, headers=temp_headers, is_iam=is_iam)
    check_response(response)
    return response


def put_request(relative_url, data, params=None, files=None, headers=None, is_iam=False):
    temp_headers = agent_headers.copy()
    if headers:
        temp_headers.update(headers)
    response = put(relative_url, data, params=params, files=files, headers=temp_headers, is_iam=is_iam)
    check_response(response)
    return response


def delete_request(relative_url, params=None, data=None, headers=None, is_iam=False):
    temp_headers = agent_headers.copy()
    if headers:
        temp_headers.update(headers)
    response = delete(relative_url, data, params=params, headers=temp_headers, is_iam=is_iam)
    check_response(response)
    return response
