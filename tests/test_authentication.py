# encoding: utf-8

"""
    tests.test_authentication

    :copyright Checkmarx
    :license MIT

"""

from CxRestAPISDK.auth import AuthenticationAPI


def test_auth():
    auth = AuthenticationAPI.AuthenticationAPI()
    assert "Bearer" in auth.auth_headers.get("Authorization")
    assert auth.auth_headers.get("Accept") == "application/json;v=1.0"
    assert auth.auth_headers.get("Content-Type") == "application/json;v=1.0"
    assert auth.auth_headers.get("cxOrigin") == "REST API"
