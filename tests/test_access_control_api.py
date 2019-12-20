

from CxRestAPISDK.accesscontrol.AccessControlAPI import AccessControlAPI


def test_get_all_assignable_users():
    ac = AccessControlAPI()
    resp = ac.get_all_assignable_users()
    assert resp is not None
    if list(resp):
        user = resp[0]
        assert user.id == 1


def test_get_all_authentication_providers():
    ac = AccessControlAPI()
    resp = ac.get_all_authentication_providers()
    assert resp is not None
    if list(resp):
        provider = resp[0]
        assert provider.id == 1


def test_submit_first_admin_user():
    ac = AccessControlAPI()
    resp = ac.submit_first_admin_user("dd", "Password01!", "Alex", "Smith", "alex.smith@test.com")
    assert resp is not None


def test_get_admin_user_exists_confirmation():
    ac = AccessControlAPI()
    resp = ac.get_admin_user_exists_confirmation()
    assert resp is True
