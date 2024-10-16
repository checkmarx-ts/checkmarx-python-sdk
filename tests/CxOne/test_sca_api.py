from CheckmarxPythonSDK.CxOne.scaAPI import ScaAPI


def test_get_projects():
    projects = ScaAPI().get_all_projects()
    assert projects is not None