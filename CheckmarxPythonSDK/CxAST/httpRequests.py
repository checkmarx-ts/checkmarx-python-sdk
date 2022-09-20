# encoding: utf-8
from .config import config
from CheckmarxPythonSDK.utilities.httpRequests import build_request_funcs, check_response


def get_data_from_config():
    server_url = config.get("server")
    token_url = config.get("access_control_url") + "/auth/realms/{TENANT_NAME}/protocol/openid-connect/token".format(
        TENANT_NAME=config.get("tenant_name")
    )
    timeout = config.get("timeout")
    verify_ssl_cert = config.get("verify")
    cert = config.get("cert")
    token_req_data = {
        "grant_type": "client_credentials",
        "username": config.get("username"),
        "password": config.get("password"),
        "client_id": config.get("client_id"),
        "client_secret": config.get("client_secret"),
    }
    if config.get("grant_type") == "refresh_token":
        token_req_data = {
            "grant_type": "refresh_token",
            "client_id": "ast-app",
            "refresh_token": config.get("refresh_token"),
        }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data


get, post, put, patch, delete = build_request_funcs(get_data_from_config)


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


def patch_request(relative_url, data):
    response = patch(relative_url, data)
    check_response(response)
    return response


def delete_request(relative_url, data=None):
    response = delete(relative_url, data)
    check_response(response)
    return response
