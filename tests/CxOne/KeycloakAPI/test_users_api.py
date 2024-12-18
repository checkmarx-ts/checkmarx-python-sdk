from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    get_users,
    get_user_id_by_name,
    get_user_id_list_by_username_list,
    get_user_id_by_email,
    get_user_id_list_by_email_list,
    create_a_new_user,
    get_number_of_users_by_given_criteria,
    delete_user,
    get_users_profile,
    get_users_profile_metadata,
    get_user_by_id,
    update_user_by_id,
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


def test_get_users_profile():
    result = get_users_profile(realm=realm)
    assert result is not None


def test_get_users_profile_metadata():
    result = get_users_profile_metadata(realm=realm)
    assert result is not None


def test_get_user_by_id():
    user_id = get_user_id_by_name(realm=realm, username="aaa")
    result = get_user_by_id(realm=realm, user_id=user_id)
    assert result is not None


def test_update_user_by_id():
    user_id = get_user_id_by_name(realm=realm, username="aaa")
    result = update_user_by_id(realm=realm, user_id=user_id, username="aaa", first_name="cup", last_name="mug",
                               email="cup@mug.com")
    assert result is True


def test_get_user_id_list_by_username_list():
    user_ids = get_user_id_list_by_username_list(realm=realm, username_list=["aaa"])
    assert len(user_ids) >= 1


def test_get_user_id_by_email():
    user_id = get_user_id_by_email(realm=realm, email="cup@mug.com")
    assert user_id is not None


def test_get_user_id_list_by_email_list():
    user_id_list = get_user_id_list_by_email_list(realm=realm, email_list=["cup@mug.com"])
    assert len(user_id_list) >= 1
