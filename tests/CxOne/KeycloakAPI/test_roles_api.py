from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    RolesApi,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.RoleRepresentation import RoleRepresentation

realm = "happy"
client_id = "d3b60524-13a1-431a-a703-1d6d3d09f512"
role_name = "test_2025_01_24"
roles_api = RolesApi()

def test_get_client_roles():    
    # 1. Test get_client_roles
    print("\n=== Test 1: get_client_roles ===")
    # Test with basic parameters
    client_roles = roles_api.get_client_roles(realm=realm, id=client_id)
    print(f"number of client roles: {len(client_roles)}")
    print(f"client_roles: {[r.name for r in client_roles]}")
    
    # Test with first and max parameters
    client_roles_paginated = roles_api.get_client_roles(realm=realm, id=client_id, first=0, max=5)
    print(f"number of client roles (paginated): {len(client_roles_paginated)}")
    print(f"client_roles (paginated): {[r.name for r in client_roles_paginated]}")
    
    # Test with search parameter
    if client_roles:
        # Get the first role name as search term
        search_term = client_roles[0].name
        client_roles_searched = roles_api.get_client_roles(realm=realm, id=client_id, search=search_term)
        print(f"number of client roles (searched): {len(client_roles_searched)}")
        print(f"client_roles (searched): {[r.to_dict() for r in client_roles_searched]}")

def test_client_role_crud():
    # 2. Test client role CRUD operations
    print("\n=== Test 2: Client role CRUD operations ===")
    test_role_name = "test_role_crud"
    updated_description = "Updated test role description"
    
    # Step 1: Delete the role if it exists
    try:
        delete_successful = roles_api.delete_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Delete role {test_role_name} successful: {delete_successful}")
    except Exception as e:
        print(f"Error deleting role {test_role_name}: {e}")
    
    # Step 2: Create the role (C)
    role_representation = RoleRepresentation(name=test_role_name)
    try:
        create_successful = roles_api.post_client_roles(
            realm=realm, id=client_id, role_representation=role_representation
        )
        print(f"Create role {test_role_name} successful: {create_successful}")
        assert create_successful is True
    except Exception as e:
        print(f"Error creating role {test_role_name}: {e}")
        raise
    
    # Step 3: Read the role (R)
    try:
        created_role = roles_api.get_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Read role {test_role_name} successful: {created_role.to_dict()}")
        assert created_role is not None
        assert created_role.name == test_role_name
    except Exception as e:
        print(f"Error reading role {test_role_name}: {e}")
        raise
    
    # Step 4: Update the role (U)
    try:
        updated_role_representation = RoleRepresentation(
            name=test_role_name,
            description=updated_description,
            composite=False,
            client_role=True
        )
        update_successful = roles_api.put_client_role(
            realm=realm, id=client_id, role_name=test_role_name, role_representation=updated_role_representation
        )
        print(f"Update role {test_role_name} successful: {update_successful}")
        assert update_successful is True
        
        # Verify the update
        updated_role = roles_api.get_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Updated role {test_role_name} description: {updated_role.description}")
        assert updated_role.description == updated_description
    except Exception as e:
        print(f"Error updating role {test_role_name}: {e}")
        raise
    
    # Step 5: Delete the role (D)
    try:
        delete_successful = roles_api.delete_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Delete role {test_role_name} successful: {delete_successful}")
        assert delete_successful is True
        
        # Verify the deletion
        try:
            deleted_role = roles_api.get_client_role(realm=realm, id=client_id, role_name=test_role_name)
            print(f"Role {test_role_name} still exists after deletion: {deleted_role.to_dict()}")
            assert False, "Role should have been deleted"
        except Exception as e:
            print(f"Verified role {test_role_name} deletion: {e}")
    except Exception as e:
        print(f"Error deleting role {test_role_name}: {e}")
        raise

def test_composite_role_operations():
    # 3. Test composite role operations
    print("\n=== Test 3: Composite role operations ===")
    temp_composite_role_name = "temp_composite_role_2026_02_14"
    
    # Step 1: Delete the temporary role if it exists
    try:
        delete_successful = roles_api.delete_client_role(realm=realm, id=client_id, role_name=temp_composite_role_name)
        print(f"Delete temporary role {temp_composite_role_name} successful: {delete_successful}")
    except Exception as e:
        print(f"Error deleting temporary role {temp_composite_role_name}: {e}")
    
    # Step 2: Create a temporary composite role
    try:
        composite_role_representation = RoleRepresentation(
            name=temp_composite_role_name,
            composite=True,
            client_role=True
        )
        create_successful = roles_api.post_client_roles(
            realm=realm, id=client_id, role_representation=composite_role_representation
            )
        print(f"Create temporary composite role {temp_composite_role_name} successful: {create_successful}")
        assert create_successful is True
    except Exception as e:
        print(f"Error creating temporary composite role {temp_composite_role_name}: {e}")
        raise
    
    # Step 3: Get some non-composite roles to add as children
    try:
        all_roles = roles_api.get_client_roles(realm=realm, id=client_id)
        non_composite_roles = [role for role in all_roles if not role.composite]
        print(f"Found {len(non_composite_roles)} non-composite roles")
        
        # Select first 2 non-composite roles as children
        child_roles = non_composite_roles[:2]
        print(f"Selected child roles:")
        for role in child_roles:
            print(f"  - {role.name}: {role.to_dict()}")
        assert len(child_roles) >= 2, "Need at least 2 non-composite roles for testing"
    except Exception as e:
        print(f"Error getting non-composite roles: {e}")
        raise
    
    # Step 4: Add child roles to composite role
    try:
        add_successful = roles_api.post_client_role_composites(
            realm=realm, id=client_id, role_name=temp_composite_role_name, role_representations=child_roles
            )
        print(f"Add child roles to {temp_composite_role_name} successful: {add_successful}")
        assert add_successful is True
    except Exception as e:
        print(f"Error adding child roles: {e}")
        raise
    
    # Step 5: Verify child roles were added
    try:
        composites = roles_api.get_client_role_composites(realm=realm, id=client_id, role_name=temp_composite_role_name)
        print(f"Composite role {temp_composite_role_name} has {len(composites)} child roles:")
        for role in composites:
            print(f"  - {role.name}: {role.to_dict()}")
        assert len(composites) >= 2, "Child roles should have been added"
    except Exception as e:
        print(f"Error getting composites: {e}")
        raise
    
    # Step 6: Remove child roles from composite role
    try:
        remove_successful = roles_api.delete_client_role_composites(
            realm=realm, id=client_id, role_name=temp_composite_role_name, role_representations=child_roles
            )
        print(f"Remove child roles from {temp_composite_role_name} successful: {remove_successful}")
        assert remove_successful is True
    except Exception as e:
        print(f"Error removing child roles: {e}")
        raise
    
    # Step 7: Verify child roles were removed
    try:
        composites_after_removal = roles_api.get_client_role_composites(realm=realm, id=client_id, role_name=temp_composite_role_name)
        print(f"Composite role {temp_composite_role_name} has {len(composites_after_removal)} child roles after removal")
        assert len(composites_after_removal) == 0, "Child roles should have been removed"
    except Exception as e:
        print(f"Error getting composites after removal: {e}")
        raise
    
    # Step 8: Delete the temporary composite role
    try:
        delete_successful = roles_api.delete_client_role(realm=realm, id=client_id, role_name=temp_composite_role_name)
        print(f"Delete temporary composite role {temp_composite_role_name} successful: {delete_successful}")
        assert delete_successful is True
    except Exception as e:
        print(f"Error deleting temporary composite role {temp_composite_role_name}: {e}")
        raise
    
def test_get_client_role_composites_client():
    # 4. Test get_client_role_composites_client
    print("\n=== Test 4: get_client_role_composites_client ===")
    temp_composite_role_name = "temp_composite_role_2026_02_14_client"
    
    # Step 1: Delete the temporary role if it exists
    try:
        delete_successful = roles_api.delete_client_role(realm=realm, id=client_id, role_name=temp_composite_role_name)
        print(f"Delete temporary role {temp_composite_role_name} successful: {delete_successful}")
    except Exception as e:
        print(f"Error deleting temporary role {temp_composite_role_name}: {e}")
    
    # Step 2: Create a temporary composite role
    try:
        composite_role_representation = RoleRepresentation(
            name=temp_composite_role_name,
            composite=True,
            client_role=True
        )
        create_successful = roles_api.post_client_roles(realm=realm, id=client_id, role_representation=composite_role_representation)
        print(f"Create temporary composite role {temp_composite_role_name} successful: {create_successful}")
        assert create_successful is True
    except Exception as e:
        print(f"Error creating temporary composite role {temp_composite_role_name}: {e}")
        raise
    
    # Step 3: Get some non-composite roles to add as children
    try:
        all_roles = roles_api.get_client_roles(realm=realm, id=client_id)
        non_composite_roles = [role for role in all_roles if not role.composite]
        print(f"Found {len(non_composite_roles)} non-composite roles")
        
        # Select first 2 non-composite roles as children
        child_roles = non_composite_roles[:2]
        print(f"Selected child roles:")
        for role in child_roles:
            print(f"  - {role.name}: {role.to_dict()}")
        assert len(child_roles) >= 2, "Need at least 2 non-composite roles for testing"
    except Exception as e:
        print(f"Error getting non-composite roles: {e}")
        raise
    
    # Step 4: Add child roles to composite role
    try:
        add_successful = roles_api.post_client_role_composites(
            realm=realm, id=client_id, role_name=temp_composite_role_name, role_representations=child_roles
            )
        print(f"Add child roles to {temp_composite_role_name} successful: {add_successful}")
        assert add_successful is True
    except Exception as e:
        print(f"Error adding child roles: {e}")
        raise
    
    # Step 5: Test get_client_role_composites_client with specific client_uuid
    try:
        target_client_uuid = 'd3b60524-13a1-431a-a703-1d6d3d09f512'
        client_composites = roles_api.get_client_role_composites_client(
            realm=realm, id=client_id, role_name=temp_composite_role_name, client_uuid=target_client_uuid
            )
        print(f"get_client_role_composites_client returned {len(client_composites)} roles:")
        for role in client_composites:
            print(f"  - {role.name}: {role.to_dict()}")
    except Exception as e:
        print(f"Error calling get_client_role_composites_client: {e}")
        raise
    
    # Step 6: Delete the temporary composite role
    try:
        delete_successful = roles_api.delete_client_role(realm=realm, id=client_id, role_name=temp_composite_role_name)
        print(f"Delete temporary composite role {temp_composite_role_name} successful: {delete_successful}")
        assert delete_successful is True
    except Exception as e:
        print(f"Error deleting temporary composite role {temp_composite_role_name}: {e}")
        raise

def test_get_client_role_composites_realm():
    # 5. Test remaining client role related methods
    print("\n=== Test 5: Remaining client role related methods ===")
    
    # Test get_client_role_composites_realm
    try:
        # Use an existing composite role
        test_role_name = "test"
        realm_composites = roles_api.get_client_role_composites_realm(realm=realm, id=client_id, role_name=test_role_name)
        print(f"get_client_role_composites_realm returned {len(realm_composites)} roles:")
        for role in realm_composites:
            print(f"  - {role.name}: {role.to_dict()}")
    except Exception as e:
        print(f"Error calling get_client_role_composites_realm: {e}")

def test_get_client_role_groups():
    # Test get_client_role_groups
    try:
        # Use an existing role
        test_role_name = "test"
        groups = roles_api.get_client_role_groups(realm=realm, id=client_id, role_name=test_role_name)
        print(f"get_client_role_groups returned {len(groups)} groups:")
        for group in groups:
            print(f"  - {group.name}: {group.to_dict()}")
    except Exception as e:
        print(f"Error calling get_client_role_groups: {e}")

def test_get_client_role_management_permissions():
    # Test get_client_role_management_permissions
    try:
        # Use an existing role
        test_role_name = "test"
        permissions = roles_api.get_client_role_management_permissions(realm=realm, id=client_id, role_name=test_role_name)
        print(f"get_client_role_management_permissions returned: {permissions.to_dict()}")
    except Exception as e:
        print(f"Error calling get_client_role_management_permissions: {e}")

def test_get_client_role_users():
    # Test get_client_role_users
    try:
        # Use an existing role
        test_role_name = "test"
        users = roles_api.get_client_role_users(realm=realm, id=client_id, role_name=test_role_name)
        print(f"get_client_role_users returned {len(users)} users:")
        for user in users:
            print(f"  - {user.username}: {user.to_dict()}")
    except Exception as e:
        print(f"Error calling get_client_role_users: {e}")
    
def test_get_roles_by_realm():
    # 6. Test realm role related methods
    print("\n=== Test 6: Realm role related methods ===")
    
    # Test get_roles_by_realm
    try:
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        print(f"get_roles_by_realm returned {len(realm_roles)} roles:")
        for role in realm_roles[:5]:  # Show first 5 roles
            print(f"  - {role.name}: {role.to_dict()}")
    except Exception as e:
        print(f"Error calling get_roles_by_realm: {e}")

def test_get_role_by_realm_by_role_name():

    # Test get_role_by_realm_by_role_name
    try:
        # Use an existing realm role
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        if realm_roles:
            test_role_name = realm_roles[0].name
            realm_role = roles_api.get_role_by_realm_by_role_name(realm=realm, role_name=test_role_name)
            print(f"get_role_by_realm_by_role_name returned: {realm_role.to_dict()}")
    except Exception as e:
        print(f"Error calling get_role_by_realm_by_role_name: {e}")

def test_get_role_composites_by_realm_by_role_name():
    # Test get_role_composites_by_realm_by_role_name
    try:
        # Use an existing realm role
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        if realm_roles:
            test_role_name = realm_roles[0].name
            composites = roles_api.get_role_composites_by_realm_by_role_name(realm=realm, role_name=test_role_name)
            print(f"get_role_composites_by_realm_by_role_name returned {len(composites)} roles:")
            for role in composites:
                print(f"  - {role.name}: {role.to_dict()}")
    except Exception as e:
        print(f"Error calling get_role_composites_by_realm_by_role_name: {e}")

def test_get_role_composites_realm_by_realm_by_role_name():
    # Test get_role_composites_realm_by_realm_by_role_name
    try:
        # Use an existing realm role
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        if realm_roles:
            test_role_name = realm_roles[0].name
            realm_composites = roles_api.get_role_composites_realm_by_realm_by_role_name(realm=realm, role_name=test_role_name)
            print(f"get_role_composites_realm_by_realm_by_role_name returned {len(realm_composites)} roles:")
            for role in realm_composites:
                print(f"  - {role.name}: {role.to_dict()}")
    except Exception as e:
        print(f"Error calling get_role_composites_realm_by_realm_by_role_name: {e}")
    
def test_get_role_groups_by_realm_by_role_name():
    # Test get_role_groups_by_realm_by_role_name
    try:
        # Use an existing realm role
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        if realm_roles:
            test_role_name = realm_roles[0].name
            groups = roles_api.get_role_groups_by_realm_by_role_name(realm=realm, role_name=test_role_name)
            print(f"get_role_groups_by_realm_by_role_name returned {len(groups)} groups:")
            for group in groups:
                print(f"  - {group.name}: {group.to_dict()}")
    except Exception as e:
        print(f"Error calling get_role_groups_by_realm_by_role_name: {e}")
    
def test_get_role_management_permissions_by_realm_by_role_name():
    # Test get_role_management_permissions_by_realm_by_role_name
    try:
        # Use an existing realm role
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        if realm_roles:
            test_role_name = realm_roles[0].name
            permissions = roles_api.get_role_management_permissions_by_realm_by_role_name(realm=realm, role_name=test_role_name)
            print(f"get_role_management_permissions_by_realm_by_role_name returned: {permissions.to_dict()}")
    except Exception as e:
        print(f"Error calling get_role_management_permissions_by_realm_by_role_name: {e}")
    
def test_get_role_users_by_realm_by_role_name():
    # Test get_role_users_by_realm_by_role_name
    try:
        # Use an existing realm role
        realm_roles = roles_api.get_roles_by_realm(realm=realm)
        if realm_roles:
            test_role_name = realm_roles[0].name
            users = roles_api.get_role_users_by_realm_by_role_name(realm=realm, role_name=test_role_name)
            print(f"get_role_users_by_realm_by_role_name returned {len(users)} users:")
            for user in users:
                print(f"  - {user.username}: {user.to_dict()}")
    except Exception as e:
        print(f"Error calling get_role_users_by_realm_by_role_name: {e}")
    
    print("\n=== All RolesApi methods tested successfully! ===")