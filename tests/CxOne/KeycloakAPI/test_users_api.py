from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    get_users,
    get_user_id_by_name,
    create_a_new_user,
    get_number_of_users_by_given_criteria,
    delete_user,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    UserRepresentation
)

realm = "happy"


def test_get_users():
    result = get_users(realm=realm)
    assert len(result) > 1
    user_id = get_user_id_by_name(realm=realm, username="test")
    assert user_id is not None


def test_get_number_of_users_by_given_criteria():
    result = get_number_of_users_by_given_criteria(realm=realm)
    assert result > 1


def test_create_and_delete_user():
    username = "user_2024-12-15"
    email = "dummy_s@happyc.com"
    first_name = "user_2024"
    last_name = "happy"
    result = create_a_new_user(realm=realm, username=username, email=email, first_name=first_name, last_name=last_name)
    assert result is True
    user_id = get_user_id_by_name(realm=realm, username=username)
    assert user_id is not None
    result = delete_user(realm=realm, user_id=user_id)
    assert result is True
