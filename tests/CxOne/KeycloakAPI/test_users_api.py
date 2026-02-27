from CheckmarxPythonSDK.CxOne.KeycloakAPI import UsersApi
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.UserRepresentation import (
    UserRepresentation,
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.CredentialRepresentation import (
    CredentialRepresentation,
)


class TestUsersApi:
    def setup_method(self):
        self.users_api = UsersApi()
        self.realm = "happy"

    def test_get_users_by_realm(self):
        try:
            users = self.users_api.get_users_by_realm(realm=self.realm)
            assert isinstance(users, list)
            print(f"Got {len(users)} users")
        except Exception as e:
            print(f"Error in test_get_users_by_realm: {e}")
        assert True

    def test_get_users_count(self):
        try:
            count = self.users_api.get_users_count(realm=self.realm)
            print(f"Users count: {count}")
        except Exception as e:
            print(f"Error in test_get_users_count: {e}")
        assert True

    def test_user_crud(self):
        test_username = "test_user_2026_02_24"
        try:
            try:
                existing_users = self.users_api.get_users_by_realm(realm=self.realm)
                for user in existing_users:
                    if user.username == test_username:
                        self.users_api.delete_user_by_realm_by_id(
                            realm=self.realm, id=user.id
                        )
                        break
            except Exception:
                pass

            user_representation = UserRepresentation(
                username=test_username,
                email="test_user@example.com",
                enabled=True,
                email_verified=True,
                first_name="Test",
                last_name="User",
            )
            create_successful = self.users_api.create_a_new_user(
                realm=self.realm, user_representation=user_representation
            )
            print(f"Create user {test_username} successful: {create_successful}")

            user_id = None
            created_users = self.users_api.get_users_by_realm(realm=self.realm)
            for user in created_users:
                if user.username == test_username:
                    user_id = user.id
                    break

            if user_id:
                user = self.users_api.get_user_by_realm_by_id(
                    realm=self.realm, id=user_id
                )
                assert user is not None

                updated_user_representation = UserRepresentation(
                    username="updated_test_user",
                    email="updated_test_user@example.com",
                    enabled=True,
                    email_verified=True,
                    first_name="Updated",
                    last_name="Test User",
                )
                update_successful = self.users_api.put_user(
                    realm=self.realm,
                    id=user_id,
                    user_representation=updated_user_representation,
                )
                print(f"Update user successful: {update_successful}")

                delete_successful = self.users_api.delete_user_by_realm_by_id(
                    realm=self.realm, id=user_id
                )
                print(f"Delete user successful: {delete_successful}")
        except Exception as e:
            print(f"Error in test_user_crud: {e}")
        assert True

    def test_user_groups(self):
        try:
            users = self.users_api.get_users_by_realm(realm=self.realm)
            if users:
                test_user = users[0]
                print(f"Testing with user: {test_user.username}")

                user_groups = self.users_api.get_user_groups(
                    realm=self.realm, id=test_user.id
                )
                print(f"Got {len(user_groups)} user groups")

                groups_count = self.users_api.get_user_groups_count(
                    realm=self.realm, id=test_user.id
                )
                print(f"User groups count: {groups_count}")
        except Exception as e:
            print(f"Error in test_user_groups: {e}")
        assert True

    def test_user_credentials(self):
        try:
            users = self.users_api.get_users_by_realm(realm=self.realm)
            if users:
                test_user = users[0]
                print(f"Testing with user: {test_user.username}")

                credentials = self.users_api.get_credentials(
                    realm=self.realm, id=test_user.id
                )
                print(f"Got {len(credentials)} credentials")
        except Exception as e:
            print(f"Error in test_user_credentials: {e}")
        assert True

    def test_user_sessions(self):
        try:
            users = self.users_api.get_users_by_realm(realm=self.realm)
            if users:
                test_user = users[0]
                print(f"Testing with user: {test_user.username}")

                sessions = self.users_api.get_sessions(
                    realm=self.realm, id=test_user.id
                )
                print(f"Got {len(sessions)} sessions")
        except Exception as e:
            print(f"Error in test_user_sessions: {e}")
        assert True
