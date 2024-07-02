from CheckmarxPythonSDK.CxRestAPISDK import GeneralAPI
from CheckmarxPythonSDK.CxRestAPISDK.sast.general.dto import CxTranslationInput

def test_get_server_license_data():
    result = GeneralAPI().get_server_license_data()
    assert result is not None


def test_get_server_system_version():
    result = GeneralAPI().get_server_system_version()
    assert result is not None


def test_get_result_states():
    result = GeneralAPI().get_result_states()
    assert result is not None


def test_create_result_state():
    result = GeneralAPI().create_result_state([CxTranslationInput(language_id=1033, name="DoesNotMakeSense")])
    assert result > 4
