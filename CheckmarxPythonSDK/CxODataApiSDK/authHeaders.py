from ..config import config
from ..auth import get_new_token
from ..CxPortalSoapApiSDK import get_version_number


def get_token():
    return get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type="password",
        scope="access_control_api sast_api",
        client_id="resource_owner_sast_client",
        client_secret="014DF517-39D1-4453-B7B3-9930C563627C"
    )


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})


is_version_bigger_than_9 = True
version_str = get_version_number().get("Version")
version_main_number = int(version_str.split()[1][0])
if version_main_number < 9:
    is_version_bigger_than_9 = False

auth_headers = {}
basic_auth = None

if is_version_bigger_than_9:
    auth_headers = {"Authorization": get_token()}
else:
    from requests.auth import HTTPBasicAuth
    basic_auth = HTTPBasicAuth(config.get("username"), config.get("password"))
