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
        "client_id": config.get("client_id"),
        "client_secret": config.get("client_secret"),
    }
    if config.get("grant_type") == "refresh_token":
        token_req_data = {
            "grant_type": "refresh_token",
            "client_id": "ast-app",
            "refresh_token": config.get("refresh_token"),
        }
    proxies = {
        "http": config.get("proxy"),
        "https": config.get("proxy"),
    }
    return server_url, token_url, timeout, verify_ssl_cert, cert, token_req_data, proxies


get, post, put, patch, delete, head = build_request_funcs(get_data_from_config)


def get_request(relative_url, params=None, headers=None, is_iam=False):
    """

    Args:
        relative_url (str):
        params (dict):
        headers (dict):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """

    response = get(relative_url, params=params, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def post_request(relative_url, data=None, params=None, json=None, files=None, headers=None, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        params (dict):
        json (object):
        headers (dict):
        files:
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = post(relative_url, data=data, params=params, json=json, files=files, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def put_request(relative_url, data=None, params=None, json=None, files=None, headers=None, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        params (dict):
        json (object):
        headers (dict):
        files:
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = put(relative_url, data=data, params=params, json=json, files=files, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def patch_request(relative_url, data=None, params=None, json=None, headers=None, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        params (dict):
        json (object):
        headers (dict):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = patch(relative_url, data=data, params=params, json=json, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def delete_request(relative_url, data=None, params=None, headers=None, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        params (dict):
        headers (dict):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = delete(relative_url, data=data, params=params, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def head_request(relative_url, params=None, headers=None, json=None, is_iam=False):
    """

    Args:
        relative_url (str):
        params (dict):
        json (object);
        headers (dict):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """

    response = head(relative_url, params=params, json=json, is_iam=is_iam, headers=headers)
    check_response(response)
    return response
