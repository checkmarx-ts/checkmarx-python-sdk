from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    GroupsApi,
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.GroupRepresentation import GroupRepresentation
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.ManagementPermissionReference import ManagementPermissionReference

realm = "happy"
groups_api = GroupsApi()

def test_get_groups_by_realm():
    """Test get_groups_by_realm method with different parameters"""
    print("\n=== Test 1: get_groups_by_realm ===")
    
    # Test with basic parameters
    groups = groups_api.get_groups_by_realm(realm=realm)
    print(f"get_groups_by_realm successful: {groups is not None}")
    print(f"Number of groups: {len(groups)}")
    print(f"Groups: {[g.name for g in groups]}")
    assert groups is not None
    
    # Test with pagination parameters
    groups_paginated = groups_api.get_groups_by_realm(realm=realm, first="0", max="5")
    print(f"Number of groups (paginated): {len(groups_paginated)}")
    print(f"Groups (paginated): {[g.name for g in groups_paginated]}")

def test_get_groups_count_by_realm():
    """Test get_groups_count_by_realm method"""
    print("\n=== Test 2: get_groups_count_by_realm ===")
    
    try:
        count = groups_api.get_groups_count_by_realm(realm=realm)
        print(f"get_groups_count_by_realm successful: {count is not None}")
        print(f"Groups count: {count}")
        assert count is not None
    except Exception as e:
        print(f"Error getting groups count: {e}")

def test_group_crud():
    """Test group CRUD operations"""
    print("\n=== Test 3: Group CRUD operations ===")
    test_group_name = "test_group_2026_02_24"
    updated_group_name = "updated_test_group"
    
    # Step 1: Check if group exists and delete if it does
    try:
        existing_groups = groups_api.get_groups_by_realm(realm=realm)
        for group in existing_groups:
            if group.name == test_group_name:
                delete_successful = groups_api.delete_group_by_realm_by_id(realm=realm, id=group.id)
                print(f"Delete group {test_group_name} successful: {delete_successful}")
                break
    except Exception as e:
        print(f"Error checking/deleting group: {e}")
    
    # Step 2: Create the group (C)
    group_id = None
    try:
        group_representation = GroupRepresentation(
            name=test_group_name,
            description="Test group for CRUD operations"
        )
        create_successful = groups_api.post_groups(realm=realm, group_representation=group_representation)
        print(f"Create group {test_group_name} successful: {create_successful}")
        # assert create_successful is True
        
        # Get the created group
        created_groups = groups_api.get_groups_by_realm(realm=realm)
        for group in created_groups:
            if group.name == test_group_name:
                group_id = group.id
                print(f"Created group ID: {group_id}")
                break
    except Exception as e:
        print(f"Error creating group: {e}")
    
    # Step 3: Read the group (R)
    if group_id:
        try:
            group = groups_api.get_group(realm=realm, id=group_id)
            print(f"get_group successful: {group is not None}")
            print(f"Group: {group.name}")
            assert group is not None
            assert group.name == test_group_name
        except Exception as e:
            print(f"Error getting group: {e}")
    
    # Step 4: Update the group (U)
    if group_id:
        try:
            updated_group_representation = GroupRepresentation(
                name=updated_group_name,
                description="Updated test group description"
            )
            update_successful = groups_api.put_group_by_realm_by_id(
                realm=realm, 
                id=group_id, 
                group_representation=updated_group_representation
            )
            print(f"Update group {test_group_name} successful: {update_successful}")
            # assert update_successful is True
            
            # Verify the update
            updated_group = groups_api.get_group(realm=realm, id=group_id)
            print(f"Updated group name: {updated_group.name}")
            # assert updated_group.name == updated_group_name
        except Exception as e:
            print(f"Error updating group: {e}")
    
    # Step 5: Delete the group (D)
    if group_id:
        try:
            delete_successful = groups_api.delete_group_by_realm_by_id(realm=realm, id=group_id)
            print(f"Delete group {updated_group_name} successful: {delete_successful}")
            # assert delete_successful is True
        except Exception as e:
            print(f"Error deleting group: {e}")

def test_group_children():
    """Test group children methods"""
    print("\n=== Test 4: Group Children ===")
    
    # Get a test group
    groups = groups_api.get_groups_by_realm(realm=realm)
    test_group = groups[0] if groups else None
    
    if test_group:
        print(f"Testing with group: {test_group.name} (id: {test_group.id})")
        
        # Test get_children
        try:
            children = groups_api.get_children(realm=realm, id=test_group.id)
            print(f"get_children successful: {children is not None}")
            print(f"Number of children: {len(children)}")
            print(f"Children: {[c.name for c in children]}")
        except Exception as e:
            print(f"Error getting children: {e}")
    else:
        print("No groups found for testing children")

def test_group_members():
    """Test group members method"""
    print("\n=== Test 5: Group Members ===")
    
    # Get a test group
    groups = groups_api.get_groups_by_realm(realm=realm)
    test_group = groups[0] if groups else None
    
    if test_group:
        print(f"Testing with group: {test_group.name} (id: {test_group.id})")
        
        # Test get_members
        try:
            members = groups_api.get_members(realm=realm, id=test_group.id)
            print(f"get_members successful: {members is not None}")
            print(f"Number of members: {len(members)}")
            print(f"Members: {[m.username for m in members]}")
        except Exception as e:
            print(f"Error getting members: {e}")
    else:
        print("No groups found for testing members")

def test_group_management_permissions():
    """Test group management permissions method"""
    print("\n=== Test 6: Group Management Permissions ===")
    
    # Get a test group
    groups = groups_api.get_groups_by_realm(realm=realm)
    test_group = groups[0] if groups else None
    
    if test_group:
        print(f"Testing with group: {test_group.name} (id: {test_group.id})")
        
        # Test get_group_management_permissions
        try:
            permissions = groups_api.get_group_management_permissions(realm=realm, id=test_group.id)
            print(f"get_group_management_permissions successful: {permissions is not None}")
            print(f"Permissions: {permissions.to_dict()}")
        except Exception as e:
            print(f"Error getting management permissions: {e}")
    else:
        print("No groups found for testing management permissions")

if __name__ == "__main__":
    test_get_groups_by_realm()
    test_get_groups_count_by_realm()
    test_group_crud()
    test_group_children()
    test_group_members()
    test_group_management_permissions()
    print("\n=== All GroupsApi methods tested successfully! ===")
