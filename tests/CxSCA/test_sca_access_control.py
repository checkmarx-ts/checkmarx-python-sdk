import pytest
from CheckmarxPythonSDK.CxScaApiSDK.AccessControlAPI import AccessControlAPI

pytestmark = pytest.mark.skip(reason="CxSCA credentials are no longer valid")


def test_get_teams():
    ac = AccessControlAPI()
    teams = ac.get_all_teams()
    assert teams is not None

