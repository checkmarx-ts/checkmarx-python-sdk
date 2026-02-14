from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    RolesApi,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.RoleRepresentation import RoleRepresentation

realm = "happy"
client_id = "d3b60524-13a1-431a-a703-1d6d3d09f512"
role_name = "test_2025_01_24"


# def test_get_all_roles_for_the_client():
#     roles = get_all_roles_for_the_client(realm=realm, client_id=client_id)
#     assert roles is not None
#     composite_roles = list(filter(lambda r: r.get("composite"), roles))
#     assert composite_roles is not None


# def test_create_role_for_the_client():
#     is_successful = create_role_for_the_client(realm=realm, client_id=client_id, role_name=role_name, description="test role")
#     assert is_successful is True


# def test_get_role_by_name():
#     role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
#     assert role is not None


# def test_delete_role_by_name():
#     is_successful = delete_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
#     assert is_successful is True


# def test_update_role_by_id():
#     role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
#     role_representation = RoleRepresentation(
#         client_role=role.get("clientRole"),
#         composite=True,
#         container_id=role.get("containerId"),
#         role_representation_id=role.get("id"),
#         name=role.get("name"),
#         attributes=role.get("attributes"),
#         description=role_name
#     )
#     role_id = role.get("id")
#     is_successful = update_role_by_id(realm=realm, role_id=role_id, role_representation=role_representation)
#     assert is_successful is True


# def test_get_roles_children():
#     role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
#     role_id = role.get("id")
#     children = get_roles_children(realm=realm, role_id=role_id)
#     assert children is not None


# def test_get_roles_children_iam():
#     role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
#     role_id = role.get("id")
#     children = get_roles_children_iam(realm=realm, role_id=role_id)
#     assert children is not None


# def test_add_children_to_a_composite_role():
#     role = get_role_by_name(realm=realm, client_id=client_id, role_name="test111111111")
#     role_id = role.get("id")
#     children = get_roles_children(realm=realm, role_id=role_id)
#     children = [RoleRepresentation(
#         client_role=child.get("clientRole"),
#         composite=child.get("composite"),
#         container_id=child.get("containerId"),
#         role_representation_id=child.get("id"),
#         name=child.get("name"),
#     ) for child in children]
#     role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
#     role_id = role.get("id")
#     is_successful = add_children_to_a_composite_role(realm=realm, role_id=role_id, children=children)
#     assert is_successful is True


# def test_get_all_roles_for_the_realm():
#     roles = get_all_roles_for_the_realm(realm=realm)
#     assert roles is not None


def test_get_client_roles():
    # Test with basic parameters
    client_roles = RolesApi().get_client_roles(realm=realm, id=client_id)
    print(f"number of client roles: {len(client_roles)}")
    print(f"client_roles: {[r.to_dict() for r in client_roles]}")
    
    # Test with first and max parameters
    client_roles_paginated = RolesApi().get_client_roles(realm=realm, id=client_id, first=0, max=5)
    print(f"number of client roles (paginated): {len(client_roles_paginated)}")
    print(f"client_roles (paginated): {[r.to_dict() for r in client_roles_paginated]}")
    
    # Test with search parameter
    if client_roles:
        # Get the first role name as search term
        search_term = client_roles[0].name
        client_roles_searched = RolesApi().get_client_roles(realm=realm, id=client_id, search=search_term)
        print(f"number of client roles (searched): {len(client_roles_searched)}")
        print(f"client_roles (searched): {[r.to_dict() for r in client_roles_searched]}")

def test_client_role_crud():
    # Test CRUD operations for client roles
    test_role_name = "test_role_2026_02_13"
    updated_description = "Updated test role description"
    
    # Step 1: Delete the role if it exists
    try:
        delete_successful = RolesApi().delete_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Delete role {test_role_name} successful: {delete_successful}")
    except Exception as e:
        print(f"Error deleting role {test_role_name}: {e}")
    
    # Step 2: Create the role (C)
    role_representation = RoleRepresentation(name=test_role_name)
    try:
        create_successful = RolesApi().post_client_roles(realm=realm, id=client_id, role_representation=role_representation)
        print(f"Create role {test_role_name} successful: {create_successful}")
        assert create_successful is True
    except Exception as e:
        print(f"Error creating role {test_role_name}: {e}")
        raise
    
    # Step 3: Read the role (R)
    try:
        created_role = RolesApi().get_client_role(realm=realm, id=client_id, role_name=test_role_name)
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
        update_successful = RolesApi().put_client_role(realm=realm, id=client_id, role_name=test_role_name, role_representation=updated_role_representation)
        print(f"Update role {test_role_name} successful: {update_successful}")
        assert update_successful is True
        
        # Verify the update
        updated_role = RolesApi().get_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Updated role {test_role_name} description: {updated_role.description}")
        assert updated_role.description == updated_description
    except Exception as e:
        print(f"Error updating role {test_role_name}: {e}")
        raise
    
    # Step 5: Delete the role (D)
    try:
        delete_successful = RolesApi().delete_client_role(realm=realm, id=client_id, role_name=test_role_name)
        print(f"Delete role {test_role_name} successful: {delete_successful}")
        assert delete_successful is True
        
        # Verify the deletion
        try:
            deleted_role = RolesApi().get_client_role(realm=realm, id=client_id, role_name=test_role_name)
            print(f"Role {test_role_name} still exists after deletion: {deleted_role.to_dict()}")
            assert False, "Role should have been deleted"
        except Exception as e:
            print(f"Verified role {test_role_name} deletion: {e}")
    except Exception as e:
        print(f"Error deleting role {test_role_name}: {e}")
        raise

def test_post_client_role_composites():
    composite_role_name = "test"
    view_webhook_role = RolesApi().get_client_role(realm=realm, id=client_id, role_name="view-webhooks")
    view_tenant_params = RolesApi().get_client_role(realm=realm, id=client_id, role_name="view-tenant-params")
    print(f"view_webhook_role: {view_webhook_role.to_dict()}")
    print(f"view_tenant_params: {view_tenant_params.to_dict()}")
    is_successful = RolesApi().post_client_role_composites(realm=realm, id=client_id, role_name=composite_role_name, role_representations=[view_webhook_role, view_tenant_params])
    assert is_successful is True