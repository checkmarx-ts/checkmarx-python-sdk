from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.api_client import ApiClient


def test_expired_token_is_refreshed_and_request_succeeds():
    """
    Integration test: inject an invalid token so the server returns 401,
    then verify the retry decorator refreshes the token and the request
    to /api/lists/states succeeds transparently.
    """
    config = construct_configuration()
    client = ApiClient(configuration=config, url_prefix="")

    # Simulate an expired token — the server will return 401 on the first attempt
    client.token_manager.current_token = "expired_invalid_token"

    url = f"{config.server_base_url}/api/lists/states"
    response = client.call_api(method="GET", url=url)

    assert response.status_code == 200
    states = response.json()
    assert states is not None
    print(f"states: {states}")
