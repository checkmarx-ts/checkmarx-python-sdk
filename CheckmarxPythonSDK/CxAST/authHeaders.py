# encoding: utf-8
import requests

from ..compat import OK
from ..config import ast_config

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def get_token():
    """
        Args:
        Returns:
            Bear Token (str)
    """
    url = ast_config.get("access_control_url") + "/auth/realms/{TENANT_NAME}/protocol/openid-connect/token".format(
        TENANT_NAME=ast_config.get("tenant_name")
    )

    req_data = {
        "grant_type":  ast_config.get("grant_type"),
        "username": ast_config.get("username"),
        "password": ast_config.get("password"),
        "client_id": ast_config.get("client_id"),
        "refresh_token": ast_config.get("refresh_token"),
    }

    response = requests.post(url=url, data=req_data, verify=False)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
