# encoding: utf-8
import requests

from CheckmarxPythonSDK.config import get_config_info

from ..compat import OK


def get_new_token(username=get_config_info().get("username"), password=get_config_info().get("password")):
    """

    Args:
        username (str):
        password (str):

    Returns:
        Bear Token (str)
    """

    token_url = get_config_info().get("base_url") + "/cxrestapi/auth/identity/connect/token"

    req_data = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "sast_api",
        "client_id": "resource_owner_sast_client",
        "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C"
    }

    response = requests.post(url=token_url, data=req_data, verify=False)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")
