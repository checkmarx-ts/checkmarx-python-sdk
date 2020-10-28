# encoding: utf-8

"""
    tests.test_authentication

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.CxRestAPISDK.authHeaders import auth_headers


def test_auth():
    assert "Bearer" in auth_headers.get("Authorization")
    assert auth_headers.get("Accept") == "application/json;v=1.0"
    assert auth_headers.get("Content-Type") == "application/json;v=1.0"
    assert auth_headers.get("cxOrigin") == "REST API"
