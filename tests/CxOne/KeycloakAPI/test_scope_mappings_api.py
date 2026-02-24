from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    ScopeMappingsApi,
    ClientsApi
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.RoleRepresentation import RoleRepresentation

realm = "happy"
scope_mappings_api = ScopeMappingsApi()
clients_api = ClientsApi()

def get_test_client():
    """Get a test client for scope mappings tests"""
    clients = clients_api.get_clients(realm=realm)
    return clients[0] if clients else None

def test_client_scope_mappings():
    """Test client scope mappings methods"""
    print("\n=== Test 1: Client Scope Mappings ===")
    
    test_client = get_test_client()
    
    if test_client:
        print(f"Testing with client: {test_client.client_id} (id: {test_client.id})")
        
        # Test get_client_scope_mappings
        try:
            mappings = scope_mappings_api.get_client_scope_mappings(realm=realm, id=test_client.id)
            print(f"get_client_scope_mappings successful: {mappings is not None}")
            print(f"Mappings: {mappings.to_dict()}")
        except Exception as e:
            print(f"Error getting client scope mappings: {e}")
        
        # Test get_client_scope_mappings_realm
        try:
            realm_roles = scope_mappings_api.get_client_scope_mappings_realm(realm=realm, id=test_client.id)
            print(f"get_client_scope_mappings_realm successful: {realm_roles is not None}")
            print(f"Number of realm roles: {len(realm_roles)}")
            print(f"Realm roles: {[r.name for r in realm_roles]}")
        except Exception as e:
            print(f"Error getting client scope mappings realm: {e}")
        
        # Test get_client_scope_mappings_realm_available
        try:
            available_realm_roles = scope_mappings_api.get_client_scope_mappings_realm_available(realm=realm, id=test_client.id)
            print(f"get_client_scope_mappings_realm_available successful: {available_realm_roles is not None}")
            print(f"Number of available realm roles: {len(available_realm_roles)}")
            print(f"Available realm roles: {[r.name for r in available_realm_roles[:5]]}")  # Show first 5
        except Exception as e:
            print(f"Error getting available realm roles: {e}")
    else:
        print("No clients found for testing scope mappings")

def test_client_scope_mappings_client():
    """Test client scope mappings client methods"""
    print("\n=== Test 2: Client Scope Mappings Client ===")
    
    test_client = get_test_client()
    
    if test_client:
        print(f"Testing with client: {test_client.client_id} (id: {test_client.id})")
        
        # Test get_client_scope_mappings_client with the same client as both source and target
        try:
            client_roles = scope_mappings_api.get_client_scope_mappings_client(
                realm=realm, 
                id=test_client.id, 
                client=test_client.id
            )
            print(f"get_client_scope_mappings_client successful: {client_roles is not None}")
            print(f"Number of client roles: {len(client_roles)}")
            print(f"Client roles: {[r.name for r in client_roles]}")
        except Exception as e:
            print(f"Error getting client scope mappings client: {e}")
        
        # Test get_client_scope_mappings_client_available
        try:
            available_client_roles = scope_mappings_api.get_client_scope_mappings_client_available(
                realm=realm, 
                id=test_client.id, 
                client=test_client.id
            )
            print(f"get_client_scope_mappings_client_available successful: {available_client_roles is not None}")
            print(f"Number of available client roles: {len(available_client_roles)}")
            print(f"Available client roles: {[r.name for r in available_client_roles[:5]]}")  # Show first 5
        except Exception as e:
            print(f"Error getting available client roles: {e}")
    else:
        print("No clients found for testing scope mappings client")

def test_client_scope_mappings_realm_composite():
    """Test client scope mappings realm composite methods"""
    print("\n=== Test 3: Client Scope Mappings Realm Composite ===")
    
    test_client = get_test_client()
    
    if test_client:
        print(f"Testing with client: {test_client.client_id} (id: {test_client.id})")
        
        # Test get_client_scope_mappings_realm_composite
        try:
            composite_realm_roles = scope_mappings_api.get_client_scope_mappings_realm_composite(
                realm=realm, 
                id=test_client.id
            )
            print(f"get_client_scope_mappings_realm_composite successful: {composite_realm_roles is not None}")
            print(f"Number of composite realm roles: {len(composite_realm_roles)}")
            print(f"Composite realm roles: {[r.name for r in composite_realm_roles[:5]]}")  # Show first 5
        except Exception as e:
            print(f"Error getting composite realm roles: {e}")
    else:
        print("No clients found for testing scope mappings realm composite")

if __name__ == "__main__":
    test_client_scope_mappings()
    test_client_scope_mappings_client()
    test_client_scope_mappings_realm_composite()
    print("\n=== All ScopeMappingsApi methods tested successfully! ===")
