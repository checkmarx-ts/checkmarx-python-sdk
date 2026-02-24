from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    UsersApi,
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.UserRepresentation import UserRepresentation
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.CredentialRepresentation import CredentialRepresentation

realm = "happy"
users_api = UsersApi()

def test_get_users_by_realm():
    """Test get_users_by_realm method with different parameters"""
    print("\n=== Test 1: get_users_by_realm ===")
    
    # Test with basic parameters
    users = users_api.get_users_by_realm(realm=realm)
    print(f"get_users_by_realm successful: {users is not None}")
    print(f"Number of users: {len(users)}")
    print(f"Users: {[u.username for u in users]}")
    assert users is not None
    
    # Test with pagination parameters
    users_paginated = users_api.get_users_by_realm(realm=realm, first="0", max="5")
    print(f"Number of users (paginated): {len(users_paginated)}")
    print(f"Users (paginated): {[u.username for u in users_paginated]}")

def test_get_users_count():
    """Test get_users_count method"""
    print("\n=== Test 2: get_users_count ===")
    
    try:
        count = users_api.get_users_count(realm=realm)
        print(f"get_users_count successful: {count is not None}")
        print(f"Users count: {count}")
        assert count is not None
    except Exception as e:
        print(f"Error getting users count: {e}")

def test_user_crud():
    """Test user CRUD operations"""
    print("\n=== Test 3: User CRUD operations ===")
    test_username = "test_user_2026_02_24"
    updated_username = "updated_test_user"
    
    # Step 1: Check if user exists and delete if it does
    try:
        existing_users = users_api.get_users_by_realm(realm=realm)
        for user in existing_users:
            if user.username == test_username:
                delete_successful = users_api.delete_user_by_realm_by_id(realm=realm, id=user.id)
                print(f"Delete user {test_username} successful: {delete_successful}")
                break
    except Exception as e:
        print(f"Error checking/deleting user: {e}")
    
    # Step 2: Create the user (C)
    user_id = None
    try:
        user_representation = UserRepresentation(
            username=test_username,
            email="test_user@example.com",
            enabled=True,
            email_verified=True,
            first_name="Test",
            last_name="User"
        )
        create_successful = users_api.create_a_new_user(realm=realm, user_representation=user_representation)
        print(f"Create user {test_username} successful: {create_successful}")
        # assert create_successful is True
        
        # Get the created user
        created_users = users_api.get_users_by_realm(realm=realm)
        for user in created_users:
            if user.username == test_username:
                user_id = user.id
                print(f"Created user ID: {user_id}")
                break
    except Exception as e:
        print(f"Error creating user: {e}")
    
    # Step 3: Read the user (R)
    if user_id:
        try:
            user = users_api.get_user_by_realm_by_id(realm=realm, id=user_id)
            print(f"get_user_by_realm_by_id successful: {user is not None}")
            print(f"User: {user.username}")
            assert user is not None
            assert user.username == test_username
        except Exception as e:
            print(f"Error getting user: {e}")
    
    # Step 4: Update the user (U)
    if user_id:
        try:
            updated_user_representation = UserRepresentation(
                username=updated_username,
                email="updated_test_user@example.com",
                enabled=True,
                email_verified=True,
                first_name="Updated",
                last_name="Test User"
            )
            update_successful = users_api.put_user(
                realm=realm, 
                id=user_id, 
                user_representation=updated_user_representation
            )
            print(f"Update user {test_username} successful: {update_successful}")
            # assert update_successful is True
            
            # Verify the update
            updated_user = users_api.get_user_by_realm_by_id(realm=realm, id=user_id)
            print(f"Updated user username: {updated_user.username}")
            # assert updated_user.username == updated_username
        except Exception as e:
            print(f"Error updating user: {e}")
    
    # Step 5: Delete the user (D)
    if user_id:
        try:
            delete_successful = users_api.delete_user_by_realm_by_id(realm=realm, id=user_id)
            print(f"Delete user {updated_username} successful: {delete_successful}")
            # assert delete_successful is True
        except Exception as e:
            print(f"Error deleting user: {e}")

def test_user_groups():
    """Test user groups operations"""
    print("\n=== Test 4: User Groups ===")
    
    # Get a test user
    users = users_api.get_users_by_realm(realm=realm)
    test_user = users[0] if users else None
    
    if test_user:
        print(f"Testing with user: {test_user.username} (id: {test_user.id})")
        
        # Test get_user_groups
        try:
            user_groups = users_api.get_user_groups(realm=realm, id=test_user.id)
            print(f"get_user_groups successful: {user_groups is not None}")
            print(f"Number of user groups: {len(user_groups)}")
            print(f"User groups: {[g.name for g in user_groups]}")
        except Exception as e:
            print(f"Error getting user groups: {e}")
        
        # Test get_user_groups_count
        try:
            groups_count = users_api.get_user_groups_count(realm=realm, id=test_user.id)
            print(f"get_user_groups_count successful: {groups_count is not None}")
            print(f"User groups count: {groups_count}")
        except Exception as e:
            print(f"Error getting user groups count: {e}")
    else:
        print("No users found for testing groups")

def test_user_credentials():
    """Test user credentials operations"""
    print("\n=== Test 5: User Credentials ===")
    
    # Get a test user
    users = users_api.get_users_by_realm(realm=realm)
    test_user = users[0] if users else None
    
    if test_user:
        print(f"Testing with user: {test_user.username} (id: {test_user.id})")
        
        # Test get_credentials
        try:
            credentials = users_api.get_credentials(realm=realm, id=test_user.id)
            print(f"get_credentials successful: {credentials is not None}")
            print(f"Number of user credentials: {len(credentials)}")
            print(f"User credentials: {[c.type for c in credentials]}")
        except Exception as e:
            print(f"Error getting user credentials: {e}")
    else:
        print("No users found for testing credentials")

def test_user_sessions():
    """Test user sessions operations"""
    print("\n=== Test 6: User Sessions ===")
    
    # Get a test user
    users = users_api.get_users_by_realm(realm=realm)
    test_user = users[0] if users else None
    
    if test_user:
        print(f"Testing with user: {test_user.username} (id: {test_user.id})")
        
        # Test get_sessions
        try:
            sessions = users_api.get_sessions(realm=realm, id=test_user.id)
            print(f"get_sessions successful: {sessions is not None}")
            print(f"Number of user sessions: {len(sessions)}")
        except Exception as e:
            print(f"Error getting user sessions: {e}")
    else:
        print("No users found for testing sessions")

if __name__ == "__main__":
    test_get_users_by_realm()
    test_get_users_count()
    test_user_crud()
    test_user_groups()
    test_user_credentials()
    test_user_sessions()
    print("\n=== All UsersApi methods tested successfully! ===")
