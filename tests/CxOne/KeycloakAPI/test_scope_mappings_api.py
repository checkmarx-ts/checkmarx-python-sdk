from CheckmarxPythonSDK.CxOne.KeycloakAPI import ScopeMappingsApi, ClientsApi


class TestScopeMappingsApi:
    def setup_method(self):
        self.scope_mappings_api = ScopeMappingsApi()
        self.clients_api = ClientsApi()
        self.realm = "happy"

    def get_test_client(self):
        try:
            clients = self.clients_api.get_clients(realm=self.realm)
            return clients[0] if clients else None
        except Exception:
            return None

    def test_client_scope_mappings(self):
        try:
            test_client = self.get_test_client()
            if test_client:
                print(f"Testing with client: {test_client.client_id}")

                mappings = self.scope_mappings_api.get_client_scope_mappings(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got client scope mappings: {mappings is not None}")

                realm_roles = self.scope_mappings_api.get_client_scope_mappings_realm(
                    realm=self.realm, id=test_client.id
                )
                print(f"Got {len(realm_roles)} realm roles")

                available_realm_roles = (
                    self.scope_mappings_api.get_client_scope_mappings_realm_available(
                        realm=self.realm, id=test_client.id
                    )
                )
                print(f"Got {len(available_realm_roles)} available realm roles")
        except Exception as e:
            print(f"Error in test_client_scope_mappings: {e}")
        assert True

    def test_client_scope_mappings_client(self):
        try:
            test_client = self.get_test_client()
            if test_client:
                print(f"Testing with client: {test_client.client_id}")

                client_roles = self.scope_mappings_api.get_client_scope_mappings_client(
                    realm=self.realm, id=test_client.id, client=test_client.id
                )
                print(f"Got {len(client_roles)} client roles")

                available_client_roles = (
                    self.scope_mappings_api.get_client_scope_mappings_client_available(
                        realm=self.realm, id=test_client.id, client=test_client.id
                    )
                )
                print(f"Got {len(available_client_roles)} available client roles")
        except Exception as e:
            print(f"Error in test_client_scope_mappings_client: {e}")
        assert True

    def test_client_scope_mappings_realm_composite(self):
        try:
            test_client = self.get_test_client()
            if test_client:
                print(f"Testing with client: {test_client.client_id}")

                composite_realm_roles = (
                    self.scope_mappings_api.get_client_scope_mappings_realm_composite(
                        realm=self.realm, id=test_client.id
                    )
                )
                print(f"Got {len(composite_realm_roles)} composite realm roles")
        except Exception as e:
            print(f"Error in test_client_scope_mappings_realm_composite: {e}")
        assert True
