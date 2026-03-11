from CheckmarxPythonSDK.CxOne import (
    AccessControlAPI,
)


def test_get_groups():
    groups = AccessControlAPI().get_groups(limit=100)
    print(f"Groups count: {len(groups)}")
    print("first 3 groups:")
    for group in groups[:3]:
        print(f"Group: {group.name}")
    assert len(groups) > 1


def test_get_group_by_name():
    group = AccessControlAPI().get_group_by_name(group_name="happy/test")
    print(f"Group: {group}")
    assert group.name == "happy/test"
    assert group.brief_name == "test"
    assert group is not None


def test_get_users():
    users = AccessControlAPI().get_users()
    print(f"Users count: {len(users)}")
    for user in users[:3]:
        print(f"User name: {user.username}")
    assert len(users) > 1


def test_get_users_by_groups():
    group = AccessControlAPI().get_group_by_name(group_name="All")
    group_id = group.id
    users = AccessControlAPI().get_users_by_groups(group_id=group_id)
    assert len(users) > 0
    print(f"Users count: {len(users)} in group All")
    for user in users[:3]:
        print(f"User name: {user.username}")


def test_get_users_count():
    users_count = AccessControlAPI().get_users_count()
    print(f"Users count: {users_count}")
    assert users_count > 0
    

def test_get_logged_in_user_roles():
    user_roles = AccessControlAPI().get_logged_in_user_roles()
    print(f"User roles count: {len(user_roles)}")
    for role in user_roles[:3]:
        print(f"Role: {role}")
    assert len(user_roles) > 0
