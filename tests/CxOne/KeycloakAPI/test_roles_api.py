from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    get_all_roles_for_the_client,
    create_role_for_the_client,
    delete_role_by_name,
    get_role_by_name,
    update_role_by_id,
    get_roles_children,
    get_roles_children_iam,
    add_children_to_a_composite_role,
    get_all_roles_for_the_realm,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    RoleRepresentation
)

realm = "happy"
client_id = "d3b60524-13a1-431a-a703-1d6d3d09f512"
role_name = "test_2025_01_24"


def test_get_all_roles_for_the_client():
    roles = get_all_roles_for_the_client(realm=realm, client_id=client_id)
    assert roles is not None
    composite_roles = list(filter(lambda r: r.get("composite"), roles))
    assert composite_roles is not None


def test_create_role_for_the_client():
    is_successful = create_role_for_the_client(realm=realm, client_id=client_id, role_name=role_name, description="test role")
    assert is_successful is True


def test_get_role_by_name():
    role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
    assert role is not None


def test_delete_role_by_name():
    is_successful = delete_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
    assert is_successful is True


def test_update_role_by_id():
    role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
    role_representation = RoleRepresentation(
        client_role=role.get("clientRole"),
        composite=True,
        container_id=role.get("containerId"),
        role_representation_id=role.get("id"),
        name=role.get("name"),
        attributes=role.get("attributes"),
        description=role_name
    )
    role_id = role.get("id")
    is_successful = update_role_by_id(realm=realm, role_id=role_id, role_representation=role_representation)
    assert is_successful is True


def test_get_roles_children():
    role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
    role_id = role.get("id")
    children = get_roles_children(realm=realm, role_id=role_id)
    assert children is not None


def test_get_roles_children_iam():
    role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
    role_id = role.get("id")
    children = get_roles_children_iam(realm=realm, role_id=role_id)
    assert children is not None


def test_add_children_to_a_composite_role():
    role = get_role_by_name(realm=realm, client_id=client_id, role_name="test111111111")
    role_id = role.get("id")
    children = get_roles_children(realm=realm, role_id=role_id)
    children = [RoleRepresentation(
        client_role=child.get("clientRole"),
        composite=child.get("composite"),
        container_id=child.get("containerId"),
        role_representation_id=child.get("id"),
        name=child.get("name"),
    ) for child in children]
    role = get_role_by_name(realm=realm, client_id=client_id, role_name=role_name)
    role_id = role.get("id")
    is_successful = add_children_to_a_composite_role(realm=realm, role_id=role_id, children=children)
    assert is_successful is True


def test_get_all_roles_for_the_realm():
    roles = get_all_roles_for_the_realm(realm=realm)
    assert roles is not None
