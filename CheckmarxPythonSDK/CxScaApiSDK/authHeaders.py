# encoding: utf-8
import requests

from ..compat import OK
from ..config import sca_config

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def get_new_token(token_url, username, password, account):
    """

    Args:
        token_url (str): US: https://platform.checkmarx.net/identity/connect/token
                         EU: https://eu.platform.checkmarx.netidentity/connect/token
        username (str): ***
        password (str): ***
        account (str): ***

    Returns:
        Bear Token (str)
    """

    req_data = {
        "username": username,
        "password": password,
        "acr_values": "Tenant:" + account,
        "grant_type": "password",
        "scope": "sca_api",
        "client_id": "sca_resource_owner",
    }

    response = requests.post(url=token_url, data=req_data, verify=False)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


def get_token():
    """

    Args:

    Returns:

    """
    return get_new_token(
        token_url=sca_config.get("access_control_url") + "/identity/connect/token",
        username=sca_config.get("username"),
        password=sca_config.get("password"),
        account=sca_config.get("account"),
    )


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
