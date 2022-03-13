# encoding: utf-8
import requests

from ..compat import OK
from .config import config
from ..auth import get_new_token

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def get_token():
    """

    Args:

    Returns:
        Bear Token (str)
    """
    return get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type="password",
        scope="reporting_api",
        client_id="reporting_service_api",
        client_secret="014DF517-39D1-4453-B7B3-9930C563627C"
    )


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
