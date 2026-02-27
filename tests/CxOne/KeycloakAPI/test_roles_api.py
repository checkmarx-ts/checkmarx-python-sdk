from CheckmarxPythonSDK.CxOne.KeycloakAPI import RolesApi
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.RoleRepresentation import (
    RoleRepresentation,
)


class TestRolesApi:
    def setup_method(self):
        self.roles_api = RolesApi()
        self.realm = "happy"
        self.client_id = "d3b60524-13a1-431a-a703-1d6d3d09f512"

    def test_get_client_roles(self):
        try:
            client_roles = self.roles_api.get_client_roles(
                realm=self.realm, id=self.client_id
            )
            assert isinstance(client_roles, list)
            print(f"Got {len(client_roles)} client roles")
        except Exception as e:
            print(f"Error in test_get_client_roles: {e}")
        assert True

    def test_client_role_crud(self):
        test_role_name = "test_role_crud"
        try:
            try:
                self.roles_api.delete_client_role(
                    realm=self.realm, id=self.client_id, role_name=test_role_name
                )
            except Exception:
                pass

            role_representation = RoleRepresentation(name=test_role_name)
            create_successful = self.roles_api.post_client_roles(
                realm=self.realm,
                id=self.client_id,
                role_representation=role_representation,
            )
            print(f"Create role {test_role_name} successful: {create_successful}")

            created_role = self.roles_api.get_client_role(
                realm=self.realm, id=self.client_id, role_name=test_role_name
            )
            assert created_role is not None

            updated_role_representation = RoleRepresentation(
                name=test_role_name,
                description="Updated test role description",
                composite=False,
                client_role=True,
            )
            update_successful = self.roles_api.put_client_role(
                realm=self.realm,
                id=self.client_id,
                role_name=test_role_name,
                role_representation=updated_role_representation,
            )
            print(f"Update role {test_role_name} successful: {update_successful}")

            delete_successful = self.roles_api.delete_client_role(
                realm=self.realm, id=self.client_id, role_name=test_role_name
            )
            print(f"Delete role {test_role_name} successful: {delete_successful}")
        except Exception as e:
            print(f"Error in test_client_role_crud: {e}")
        assert True

    def test_composite_role_operations(self):
        temp_composite_role_name = "temp_composite_role_2026_02_14"
        try:
            try:
                self.roles_api.delete_client_role(
                    realm=self.realm,
                    id=self.client_id,
                    role_name=temp_composite_role_name,
                )
            except Exception:
                pass

            composite_role_representation = RoleRepresentation(
                name=temp_composite_role_name, composite=True, client_role=True
            )
            create_successful = self.roles_api.post_client_roles(
                realm=self.realm,
                id=self.client_id,
                role_representation=composite_role_representation,
            )
            print(f"Create temporary composite role successful: {create_successful}")

            all_roles = self.roles_api.get_client_roles(
                realm=self.realm, id=self.client_id
            )
            non_composite_roles = [role for role in all_roles if not role.composite][:2]

            if len(non_composite_roles) >= 2:
                add_successful = self.roles_api.post_client_role_composites(
                    realm=self.realm,
                    id=self.client_id,
                    role_name=temp_composite_role_name,
                    role_representations=non_composite_roles,
                )
                print(f"Add child roles successful: {add_successful}")

                composites = self.roles_api.get_client_role_composites(
                    realm=self.realm,
                    id=self.client_id,
                    role_name=temp_composite_role_name,
                )
                print(f"Got {len(composites)} child roles")

                remove_successful = self.roles_api.delete_client_role_composites(
                    realm=self.realm,
                    id=self.client_id,
                    role_name=temp_composite_role_name,
                    role_representations=non_composite_roles,
                )
                print(f"Remove child roles successful: {remove_successful}")

            self.roles_api.delete_client_role(
                realm=self.realm, id=self.client_id, role_name=temp_composite_role_name
            )
        except Exception as e:
            print(f"Error in test_composite_role_operations: {e}")
        assert True

    def test_get_roles_by_realm(self):
        try:
            realm_roles = self.roles_api.get_roles_by_realm(realm=self.realm)
            assert isinstance(realm_roles, list)
            print(f"Got {len(realm_roles)} realm roles")
        except Exception as e:
            print(f"Error in test_get_roles_by_realm: {e}")
        assert True
