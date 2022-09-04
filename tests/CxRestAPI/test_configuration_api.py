from CheckmarxPythonSDK.CxRestAPISDK import ConfigurationAPI
from CheckmarxPythonSDK.CxRestAPISDK.sast.configuration.dto import CxSASTConfig


def test_get_cx_component_configuration_settings():
    configuration_api = ConfigurationAPI()
    response = configuration_api.get_cx_component_configuration_settings('SystemSettings')
    assert len(response) > 1


def test_update_cx_component_configuration_settings():
    configuration_api = ConfigurationAPI()
    group = "SystemSettings"

    key_value_list = [
        {
            "key": "MAXIMUM_CONCURRENT_SCAN_EXECUTERS",
            "value": "2"
        }
    ]
    response = configuration_api.update_cx_component_configuration_settings(
        group=group, key_value_list=key_value_list
    )
    assert response is True


def test_update_cx_component_configuration_settings_with_param_cxsast_config():
    configuration_api = ConfigurationAPI()
    group = "SystemSettings"
    key_value_list = [
        CxSASTConfig(key="MAXIMUM_CONCURRENT_SCAN_EXECUTERS", value="2"),
    ]
    response = configuration_api.update_cx_component_configuration_settings(
        group=group, key_value_list=key_value_list
    )
    assert response is True
