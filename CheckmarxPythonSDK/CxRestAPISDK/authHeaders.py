from ..config import config
from ..auth import get_new_token
from ..__version__ import __version__


def get_token():
    return get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type="password",
        scope=config.get("scope"),
        client_id="resource_owner_client",
        client_secret="014DF517-39D1-4453-B7B3-9930C563627C"
    )


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
    "cxOrigin": "Checkmarx Python SDK " + __version__
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
