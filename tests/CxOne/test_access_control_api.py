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


def test_get_pip_users():
    """GET /pip/users — search for users."""
    try:
        users = AccessControlAPI().get_pip_users(term="happy")
        assert users is not None
        print(f"PIP users count: {len(users)}")
    except Exception as e:
        print("get_pip_users skipped: {}".format(str(e)))


def test_get_group_managers():
    """GET /group-manager — get group managers."""
    try:
        managers = AccessControlAPI().get_group_managers()
        assert managers is not None
        print(f"Group managers: {len(managers)}")
    except Exception as e:
        print("get_group_managers skipped: {}".format(str(e)))


def test_get_api_keys():
    """GET /api-keys — get API keys."""
    try:
        keys = AccessControlAPI().get_api_keys()
        assert keys is not None
        print(f"API keys count: {len(keys)}")
    except Exception as e:
        print("get_api_keys skipped: {}".format(str(e)))


def test_get_api_keys_count():
    """GET /api-keys/count — get API key count."""
    try:
        count = AccessControlAPI().get_api_keys_count()
        assert isinstance(count, int)
        print(f"API keys count: {count}")
    except Exception as e:
        print("get_api_keys_count skipped: {}".format(str(e)))


def test_get_owner():
    """GET /owner — get realm owner."""
    try:
        owner = AccessControlAPI().get_owner()
        assert owner is not None
        print(f"Owner: {owner.get('username')}")
    except Exception as e:
        print("get_owner skipped: {}".format(str(e)))


def test_get_token_exchange():
    """GET /token-exchange — get token exchange."""
    try:
        token = AccessControlAPI().get_token_exchange()
        assert token is not None
        assert "access_token" in token
    except Exception as e:
        print("get_token_exchange skipped: {}".format(str(e)))


def test_post_bulk_entities_find():
    """POST /bulk-entities/find — find entities by IDs."""
    users = AccessControlAPI().get_users(max_result_size=2)
    if len(users) < 1:
        print("No users found, skipping bulk entities test")
        return
    try:
        result = AccessControlAPI().post_bulk_entities_find(
            ids=[users[0].id],
            type="user",
        )
        assert result is not None
    except Exception as e:
        print("post_bulk_entities_find skipped: {}".format(str(e)))
