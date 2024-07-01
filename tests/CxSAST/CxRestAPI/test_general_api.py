from CheckmarxPythonSDK.CxRestAPISDK import GeneralAPI


def test_get_server_license_data():
    result = GeneralAPI().get_server_license_data()
    assert result is not None


def test_get_server_system_version():
    result = GeneralAPI().get_server_system_version()
    assert result is not None


def test_get_result_states():
    result = GeneralAPI().get_result_states()
    assert result is not None
