# encoding: utf-8
import requests

from CheckmarxPythonSDK.utilities.compat import OK
from .config import config

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def get_token():
    """
        Args:
        Returns:
            Bear Token (str)
    """
    url = config.get("access_control_url") + "/auth/realms/{TENANT_NAME}/protocol/openid-connect/token".format(
        TENANT_NAME=config.get("tenant_name")
    )
    req_data = {
        "grant_type": "client_credentials",
        "username": config.get("username"),
        "password": config.get("password"),
        "client_id": config.get("client_id"),
        "client_secret": config.get("client_secret"),
    }
    if config.get("grant_type") == "refresh_token":
        req_data = {
            "grant_type": "refresh_token",
            "client_id": "ast-app",
            "refresh_token": config.get("refresh_token"),
        }

    response = requests.post(url=url, data=req_data, verify=False)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json; version=1.0",
    "Content-Type": "application/json; version=1.0",
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
