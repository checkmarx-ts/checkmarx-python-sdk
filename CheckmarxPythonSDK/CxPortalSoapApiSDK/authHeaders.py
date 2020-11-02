from ..config import config
from ..auth import get_new_token

auth_headers = {}


def get_token():
    return get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type="password",
        scope="sast_api",
        client_id="resource_owner_sast_client",
        client_secret="014DF517-39D1-4453-B7B3-9930C563627C"
    )


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
