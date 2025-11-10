from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    UsersApi,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    UserRepresentation
)

realm = "happy"


def test_get_users():
    result = UsersApi().get_users_by_realm(realm=realm)
    assert len(result) > 1
    # user_id = UsersApi().get_user_id_by_name(realm=realm, username="test")
    # assert user_id is not None


def test_get_number_of_users_by_given_criteria():
    result = UsersApi().get_users_count(realm=realm)
    assert result > 1


def test_create_and_delete_user():
    username = "user_2024-12-15"
    email = "dummy_s@happyc.com"
    first_name = "user_2024"
    last_name = "happy"
    result = UsersApi().create_a_new_user(realm=realm, user_representation=UserRepresentation(username=username, email=email, first_name=first_name, last_name=last_name))
    assert result is True
    users = UsersApi().get_users_by_realm(realm=realm, username=username)
    assert users[0].id is not None
    result = UsersApi().delete_user_by_realm_by_id(realm=realm, id=users[0].id)
    assert result is True


def test_get_users_profile():
    result = UsersApi().get_profile(realm=realm)
    assert result is not None


def test_get_users_profile_metadata():
    result = UsersApi().get_metadata(realm=realm)
    assert result is not None

#
# def test_update_user_by_id():
#     user_id = get_user_id_by_name(realm=realm, username="aaa")
#     result = update_user_by_id(realm=realm, user_id=user_id, username="aaa", first_name="cup", last_name="mug",
#                                email="cup@mug.com")
#     assert result is True
#
#
# def test_get_user_id_list_by_username_list():
#     user_ids = get_user_id_list_by_username_list(realm=realm, username_list=["aaa"])
#     assert len(user_ids) >= 1
#
#
# def test_get_user_id_by_email():
#     user_id = get_user_id_by_email(realm=realm, email="cup@mug.com")
#     assert user_id is not None
#
#
# def test_get_user_id_list_by_email_list():
#     user_id_list = get_user_id_list_by_email_list(realm=realm, email_list=["cup@mug.com"])
#     assert len(user_id_list) >= 1
