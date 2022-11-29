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

headers = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/106.0.0.0 Safari/537.36"
}


def get_request(relative_url, is_iam=False):
    """

    Args:
        relative_url (str):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """

    response = get(relative_url, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def post_request(relative_url, data, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = post(relative_url, data, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def put_request(relative_url, data, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = put(relative_url, data, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def patch_request(relative_url, data, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = patch(relative_url, data, is_iam=is_iam, headers=headers)
    check_response(response)
    return response


def delete_request(relative_url, data=None, is_iam=False):
    """

    Args:
        relative_url (str):
        data (str):
        is_iam (bool): True if the endpoint is for Identity And Management

    Returns:

    """
    response = delete(relative_url, data, is_iam=is_iam, headers=headers)
    check_response(response)
    return response
