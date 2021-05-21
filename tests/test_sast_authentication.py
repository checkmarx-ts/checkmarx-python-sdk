# encoding: utf-8

"""
    tests.test_authentication

    :copyright Checkmarx
    :license MIT

"""

import CheckmarxPythonSDK.CxRestAPISDK.authHeaders as sastAuth
import CheckmarxPythonSDK.CxIAST.authHeaders as iastAuth


def test_sast_auth():
    assert "Bearer" in sastAuth.auth_headers.get("Authorization")
    assert sastAuth.auth_headers.get("Accept") == "application/json;v=1.0"
    assert sastAuth.auth_headers.get("Content-Type") == "application/json;v=1.0"
    assert "Checkmarx Python SDK" in sastAuth.auth_headers.get("cxOrigin")


def test_iast_auth():
    assert "Bearer" in iastAuth.auth_headers.get("Authorization")
    assert iastAuth.auth_headers.get("Accept") == "application/json;v=1.0"
    assert iastAuth.auth_headers.get("Content-Type") == "application/json;v=1.0"
    assert "Checkmarx Python SDK" in iastAuth.auth_headers.get("cxOrigin")
