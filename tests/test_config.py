# encoding: utf-8

"""
    tests.test_config

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.config import config


def test_config_from_file():

    assert config.get("grant_type") == "password"
    assert config.get("scope") == "sast_rest_api"
    assert config.get("client_id") == "resource_owner_client"
    assert config.get("client_secret") == "014DF517-39D1-4453-B7B3-9930C563627C"
    assert config.get("team_full_name") == "/CxServer"
    assert config.get("username") is not None
    assert config.get("password") is not None
    assert config.get("base_url") is not None
