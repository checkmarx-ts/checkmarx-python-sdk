from CheckmarxPythonSDK.CxOne.AccessControlAPI import (
    get_groups,
    get_users,
    get_users_by_groups,
    get_group_by_name,
    # get_api_keys,
)

realm = "asean_2021_08"


def test_get_groups():

    groups = get_groups(realm=realm)
    assert len(groups) > 1


def test_get_sub_group():
    group = get_group_by_name(realm=realm, group_name="dev/alpha")
    assert group is not None


def test_get_users():
    users = get_users(realm=realm, term=None)
    assert len(users) > 1


def test_get_users_by_groups():
    # "CSM-Group"
    group_id = '36e79d6f-ce11-4a5c-91d3-53a3661e76f4'
    users = get_users_by_groups(realm=realm, group_id=group_id)
    assert len(users) > 1
