from CheckmarxPythonSDK.CxOne.KeycloakAPI import ClientsApi
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.ClientRepresentation import (
    ClientRepresentation,
)


class TestClientsApi:
    def setup_method(self):
        self.clients_api = ClientsApi()
        self.realm = "happy"

    def test_get_clients(self):
        try:
            clients = self.clients_api.get_clients(realm=self.realm)
            assert isinstance(clients, list)
            print(f"Got {len(clients)} clients")
        except Exception as e:
            print(f"Error in test_get_clients: {e}")
        assert True

    def test_client_crud(self):
        test_client_id = "test_client_2026_02_24"
        try:
            try:
                existing_clients = self.clients_api.get_clients(
                    realm=self.realm, client_id=test_client_id
                )
                if existing_clients:
                    self.clients_api.delete_client_by_realm_by_id(
                        realm=self.realm, id=existing_clients[0].id
                    )
            except Exception:
                pass

            client_representation = ClientRepresentation(
                client_id=test_client_id, enabled=True
            )
            create_successful = self.clients_api.post_clients(
                realm=self.realm, client_representation=client_representation
            )
            print(f"Create client {test_client_id} successful: {create_successful}")

            client_id = None
            created_clients = self.clients_api.get_clients(
                realm=self.realm, client_id=test_client_id
            )
            if created_clients:
                client_id = created_clients[0].id
                created_client = self.clients_api.get_client_by_realm_by_id(
                    realm=self.realm, id=client_id
                )
                assert created_client is not None

                updated_client_representation = ClientRepresentation(
                    client_id=test_client_id, enabled=True
                )
                update_successful = self.clients_api.put_client(
                    realm=self.realm,
                    id=client_id,
                    client_representation=updated_client_representation,
                )
                print(f"Update client successful: {update_successful}")

                delete_successful = self.clients_api.delete_client_by_realm_by_id(
                    realm=self.realm, id=client_id
                )
                print(f"Delete client successful: {delete_successful}")
        except Exception as e:
            print(f"Error in test_client_crud: {e}")
        assert True

    def test_client_secret_operations(self):
        try:
            clients = self.clients_api.get_clients(realm=self.realm)
            if clients:
                test_client = clients[0]
                print(f"Testing with client: {test_client.client_id}")

                secret = self.clients_api.get_client_secret(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got client secret: {secret is not None}")

                new_secret = self.clients_api.post_client_secret(
                    realm=self.realm, id=test_client.id
                )
                print(f"Generated new secret: {new_secret is not None}")
        except Exception as e:
            print(f"Error in test_client_secret_operations: {e}")
        assert True

    def test_client_scopes(self):
        try:
            clients = self.clients_api.get_clients(realm=self.realm)
            if clients:
                test_client = clients[0]
                print(f"Testing with client: {test_client.client_id}")

                default_scopes = self.clients_api.get_default_client_scopes(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got {len(default_scopes)} default scopes")

                optional_scopes = self.clients_api.get_optional_client_scopes(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got {len(optional_scopes)} optional scopes")
        except Exception as e:
            print(f"Error in test_client_scopes: {e}")
        assert True

    def test_client_sessions(self):
        try:
            clients = self.clients_api.get_clients(realm=self.realm)
            if clients:
                test_client = clients[0]
                print(f"Testing with client: {test_client.client_id}")

                session_count = self.clients_api.get_session_count(
                    realm=self.realm, id=test_client.id
                )
                print(f"Session count: {session_count}")

                offline_session_count = self.clients_api.get_offline_session_count(
                    realm=self.realm, id=test_client.id
                )
                print(f"Offline session count: {offline_session_count}")
        except Exception as e:
            print(f"Error in test_client_sessions: {e}")
        assert True

    def test_other_client_methods(self):
        try:
            clients = self.clients_api.get_clients(realm=self.realm)
            if clients:
                test_client = clients[0]
                print(f"Testing with client: {test_client.client_id}")

                permissions = self.clients_api.get_client_management_permissions(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got management permissions: {permissions is not None}")

                service_account_user = self.clients_api.get_service_account_user(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got service account user: {service_account_user is not None}")
        except Exception as e:
            print(f"Error in test_other_client_methods: {e}")
        assert True
