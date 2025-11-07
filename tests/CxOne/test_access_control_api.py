from CheckmarxPythonSDK.CxOne import (
    AccessControlAPI,
)

realm = "happy"


def test_get_groups():
    groups = AccessControlAPI().get_groups(realm=realm, limit=100)
    assert len(groups) > 1


def test_get_group_by_name():
    group = AccessControlAPI().get_group_by_name(realm=realm, group_name="happy/test")
    assert group is not None


def test_get_users():
    users = AccessControlAPI().get_users(realm=realm)
    assert len(users) > 1


def test_get_users_by_groups():
    group_id = 'ba2d28a4-aac7-4859-90ed-e9fbfc62d947'
    users = AccessControlAPI().get_users_by_groups(realm=realm, group_id=group_id)
    assert len(users) > 0


def test_get_users_count():
    users_count = AccessControlAPI().get_users_count(realm=realm)
    assert users_count > 0


def test_get_logged_in_user_roles():
    user_roles = AccessControlAPI().get_logged_in_user_roles(realm=realm)
    assert len(user_roles) > 0
