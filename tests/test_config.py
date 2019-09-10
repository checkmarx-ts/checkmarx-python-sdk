# encoding: utf-8

"""
    tests.test_config

    :copyright Checkmarx
    :license MIT

"""

from CxRestAPISDK.config import CxConfig


def test_config_from_file():
    config = CxConfig.CxConfig()
    assert config.grant_type == "password"
    assert config.scope == "sast_rest_api"
    assert config.client_id == "resource_owner_client"
    assert config.client_secret == "014DF517-39D1-4453-B7B3-9930C563627C"
    assert config.team_full_name == "/CxServer/SP/Company/Users"
    assert config.username is not None
    assert config.password is not None
    assert config.base_url is not None
