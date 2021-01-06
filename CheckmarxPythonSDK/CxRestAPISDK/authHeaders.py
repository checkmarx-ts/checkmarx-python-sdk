from ..config import config
from ..auth import get_new_token
from ..__version__ import __version__


def get_token(with_ac=False):
    """

    Args:
        with_ac (bool): with access control or not

    Returns:

    """
    scope = "sast_rest_api"
    if with_ac:
        scope = "sast_rest_api access_control_api"

    return get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type="password",
        scope=scope,
        client_id="resource_owner_client",
        client_secret="014DF517-39D1-4453-B7B3-9930C563627C"
    )


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
    "cxOrigin": "Checkmarx Python SDK " + __version__
}


def update_auth_headers(with_ac=False):
    auth_headers.update({"Authorization": get_token(with_ac)})


def get_v2_headers():
    headers = auth_headers.copy()
    headers["Accept"] = "application/json;v=2.0"
    headers["Content-Type"] = "application/json;v=2.0"
    return headers
