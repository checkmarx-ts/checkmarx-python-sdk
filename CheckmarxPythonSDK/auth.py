# encoding: utf-8
import requests

from .compat import OK

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def get_new_token(base_url, username, password, grant_type, scope, client_id, client_secret):
    """

    Args:
        base_url (str): "ttp://localhost"
        username (str): ***
        password (str): ***
        grant_type (str): "password"
        scope (str): "sast_api"
        client_id (str): "resource_owner_client" or "resource_owner_sast_client"
        client_secret (str): "014DF517-39D1-4453-B7B3-9930C563627C"

    Returns:
        Bear Token (str)
    """

    token_url = base_url + "/cxrestapi/auth/identity/connect/token"

    req_data = {
        "username": username,
        "password": password,
        "grant_type": grant_type,
        "scope": scope,
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url=token_url, data=req_data, verify=False)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")
