from CheckmarxPythonSDK.CxScaApiSDK import authHeaders


def test_auth():
    auth_headers = authHeaders.auth_headers
    assert auth_headers is not None
