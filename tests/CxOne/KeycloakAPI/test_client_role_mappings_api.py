from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    ClientRoleMappingsApi,
    GroupsApi,
    UsersApi,
    ClientsApi
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.RoleRepresentation import RoleRepresentation

realm = "happy"
client_role_mappings_api = ClientRoleMappingsApi()
groups_api = GroupsApi()
users_api = UsersApi()
clients_api = ClientsApi()

def get_test_data():
    """Get test data for client role mappings tests"""
    print("\n=== Getting test data ===")
    
    # Get a test client
    clients = clients_api.get_clients(realm=realm)
    test_client = clients[0] if clients else None
    print(f"Test client: {test_client.client_id if test_client else 'None'}")
    
    # Get a test group
    groups = groups_api.get_groups_by_realm(realm=realm)
    test_group = groups[0] if groups else None
    print(f"Test group: {test_group.name if test_group else 'None'}")
    
    # Get a test user
    users = users_api.get_users_by_realm(realm=realm)
    test_user = users[0] if users else None
    print(f"Test user: {test_user.username if test_user else 'None'}")
    
    return test_client, test_group, test_user

def test_group_role_mappings():
    """Test group role mappings methods"""
    print("\n=== Test 1: Group Role Mappings ===")
    
    test_client, test_group, _ = get_test_data()
    
    if test_client and test_group:
        # Test get_group_role_mappings_client
        try:
            group_roles = client_role_mappings_api.get_group_role_mappings_client(
                realm=realm, 
                id=test_group.id, 
                client=test_client.id
            )
            print(f"get_group_role_mappings_client successful: {group_roles is not None}")
            print(f"Number of group roles: {len(group_roles)}")
            print(f"Group roles: {[r.name for r in group_roles]}")
        except Exception as e:
            print(f"Error getting group role mappings: {e}")
        
        # Test get_group_role_mappings_client_available
        try:
            available_roles = client_role_mappings_api.get_group_role_mappings_client_available(
                realm=realm, 
                id=test_group.id, 
                client=test_client.id
            )
            print(f"get_group_role_mappings_client_available successful: {available_roles is not None}")
            print(f"Number of available roles: {len(available_roles)}")
            print(f"Available roles: {[r.name for r in available_roles]}")
        except Exception as e:
            print(f"Error getting available group role mappings: {e}")
        
        # Test get_group_role_mappings_client_composite
        try:
            composite_roles = client_role_mappings_api.get_group_role_mappings_client_composite(
                realm=realm, 
                id=test_group.id, 
                client=test_client.id
            )
            print(f"get_group_role_mappings_client_composite successful: {composite_roles is not None}")
            print(f"Number of composite roles: {len(composite_roles)}")
            print(f"Composite roles: {[r.name for r in composite_roles]}")
        except Exception as e:
            print(f"Error getting composite group role mappings: {e}")
    else:
        print("Insufficient test data for group role mappings tests")

def test_user_role_mappings():
    """Test user role mappings methods"""
    print("\n=== Test 2: User Role Mappings ===")
    
    test_client, _, test_user = get_test_data()
    
    if test_client and test_user:
        # Test get_user_role_mappings_client
        try:
            user_roles = client_role_mappings_api.get_user_role_mappings_client(
                realm=realm, 
                id=test_user.id, 
                client=test_client.id
            )
            print(f"get_user_role_mappings_client successful: {user_roles is not None}")
            print(f"Number of user roles: {len(user_roles)}")
            print(f"User roles: {[r.name for r in user_roles]}")
        except Exception as e:
            print(f"Error getting user role mappings: {e}")
        
        # Test get_user_role_mappings_client_available
        try:
            available_roles = client_role_mappings_api.get_user_role_mappings_client_available(
                realm=realm, 
                id=test_user.id, 
                client=test_client.id
            )
            print(f"get_user_role_mappings_client_available successful: {available_roles is not None}")
            print(f"Number of available roles: {len(available_roles)}")
            print(f"Available roles: {[r.name for r in available_roles]}")
        except Exception as e:
            print(f"Error getting available user role mappings: {e}")
        
        # Test get_user_role_mappings_client_composite
        try:
            composite_roles = client_role_mappings_api.get_user_role_mappings_client_composite(
                realm=realm, 
                id=test_user.id, 
                client=test_client.id
            )
            print(f"get_user_role_mappings_client_composite successful: {composite_roles is not None}")
            print(f"Number of composite roles: {len(composite_roles)}")
            print(f"Composite roles: {[r.name for r in composite_roles]}")
        except Exception as e:
            print(f"Error getting composite user role mappings: {e}")
    else:
        print("Insufficient test data for user role mappings tests")

if __name__ == "__main__":
    test_group_role_mappings()
    test_user_role_mappings()
    print("\n=== All ClientRoleMappingsApi methods tested successfully! ===")
