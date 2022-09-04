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
        "acr_values": "Tenant:" + account,
        "grant_type": "password",
        "scope": scope,
        "client_id": "sca_resource_owner",
    }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data


get, post, put, _, delete = build_request_funcs(get_data_from_config)


def get_request(relative_url):
    response = get(relative_url)
    check_response(response)
    return response


def post_request(relative_url, data):
    response = post(relative_url, data)
    check_response(response)
    return response


def put_request(relative_url, data):
    response = put(relative_url, data)
    check_response(response)
    return response


def delete_request(relative_url, data=None):
    response = delete(relative_url, data)
    check_response(response)
    return response
