from CheckmarxPythonSDK.CxRestAPISDK import GeneralAPI


def test_get_server_system_version():
    result = GeneralAPI().get_server_system_version()
    assert result is not None