from CheckmarxPythonSDK.CxOne import VersionsAPI


def test_versions_api():
    response = VersionsAPI().get_versions_from_engines()
    assert "9.7.4" in response.sast
