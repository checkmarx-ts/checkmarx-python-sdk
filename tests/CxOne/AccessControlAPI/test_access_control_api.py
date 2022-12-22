from CheckmarxPythonSDK.CxOne.AccessControlAPI.api import (
    get_groups
)


def test_get_groups():
    realm = "asean_2021_08"
    groups = get_groups(realm=realm)
    assert len(groups) > 1
