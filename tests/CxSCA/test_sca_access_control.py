from CheckmarxPythonSDK.CxScaApiSDK.AccessControlAPI import AccessControlAPI


def test_get_teams():
    ac = AccessControlAPI()
    teams = ac.get_all_teams()
    assert teams is not None

