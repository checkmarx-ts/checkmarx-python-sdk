from CheckmarxPythonSDK.CxAST import (
    get_realms,
    get_users,
)


def test_get_realms():
    realms = get_realms()
    assert realms is not None


def test_get_users():
    users = get_users(realm="asean_2021_08")
    assert users is not None
