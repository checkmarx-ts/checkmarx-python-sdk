from CheckmarxPythonSDK.CxAST import (
    get_realms,
    get_users,
    create_a_new_user,
)
from CheckmarxPythonSDK.CxAST.KeycloakAPI.dto import (
    UserRepresentation
)

realm = "asean_2021_08"


def test_get_realms():
    realms = get_realms()
    assert realms is not None


def test_get_users():
    users = get_users(realm=realm)
    assert users is not None


def test_create_new_user():
    user_representation = UserRepresentation(username="alex", email="yang2149@163.com", first_name="test",
                                             last_name="test")
    response = create_a_new_user(realm=realm, user_representation=user_representation)
    assert response is True
