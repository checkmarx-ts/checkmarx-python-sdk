from CheckmarxPythonSDK.CxRestAPISDK.httpRequests import get_data_from_config
from CheckmarxPythonSDK.utilities.httpRequests import get_new_token

auth_headers = {}


def get_token():
    _, token_url, timeout, verify_ssl_cert, cert, token_req_data = get_data_from_config()
    token_req_data.update(
        {
            "grant_type": "password",
            "scope": "sast_api",
            "client_id": "resource_owner_sast_client",
            "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C",
        }
    )
    return get_new_token(token_url, token_req_data, timeout=timeout, verify_ssl_cert=verify_ssl_cert, cert=cert)


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
