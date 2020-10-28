from ..auth import get_new_token
from .. import __version__

auth_headers = {
    "Authorization": get_new_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
    "cxOrigin": "Checkmarx Python SDK " + __version__
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_new_token()})
