
from CheckmarxPythonSDK.CxOne import (
    AccessManagementAPI,
    create_an_assignment,
    delete_an_assignment,
    retrieve_an_assignment,
    update_assignment_roles,
    retrieve_resource_assignments,
    create_multiple_assignments,
    add_roles_to_assignment,
    retrieve_entities,
    retrieve_extended_entities_for_resource,
    retrieve_resources,
    check_access,
    check_access_to_requested_groups,
    retrieve_accessible_resources,
    retrieve_users_with_resources,
    retrieve_clients_with_resources,
    retrieve_groups_with_resources,
    get_a_list_of_permissions_of_entity_for_resource,
    get_a_list_of_applications_with_action_for_user_or_client,
    get_a_list_of_projects_with_action_for_user_or_client,
    retrieve_user_or_client_groups,
    retrieve_user_or_client_available_groups,
    retrieve_groups,
    retrieve_users,
    retrieve_clients,
    retrieve_users_from_internal_am_storage,
    retrieve_groups_from_internal_am_storage,
    retrieve_clients_from_internal_am_storage,
    retrieve_entity_base_roles,
    update_base_roles_for_an_entity,
    assign_base_roles_to_an_entity,
    delete_base_roles_for_an_entity,
    assign_base_roles_by_role_name,
    unassign_base_roles_by_role_name,
    retrieve_roles,
    create_a_role,
    retrieve_role,
    update_a_role,
    delete_a_role,
    retrieve_permissions,
)

from CheckmarxPythonSDK.CxOne.dto import (
    AssignmentInput,
    AssignmentsForResource,
    Assignment,
    MultipleAssignmentInput,
    AddAssignmentRoles,
    ResourcesResponse,
    UsersWithResourcesResponse,
    ClientsWithResourcesResponse,
    GroupsWithResourcesResponse,
    Role,
    BaseRolesResponse,
    BaseRolesRequest,
    RoleWithDetails,
    Permission,
    EntityRolesRequest,
    CreateRoleRequest,
    Error,
    GroupsResponse,
    GroupRepresentation,
    Group,
    User,
    Client,
    InternalUser,
    InternalGroup,
    InternalClient,
    ProtocolMappersRepresentation,
    EffectivePermissionsForResourceResponse,
    EntitiesForExtendedResponse,
    Rule,
    Application,
    ApplicationsCollection,
    Project,
    ProjectsCollection,
    EntityType,
    ResourceType,
)


def test_create_an_assignment():
    result = create_an_assignment(
        assignment_input=AssignmentInput(
            entity_id="3a7cf5fc-6554-4136-918b-6f494656b2b0",
            entity_type=EntityType.GROUP,
            resource_id="71fe66b9-b3ea-4fc7-8594-541d0a07a697",
            resource_type=ResourceType.TENANT,
            entity_roles=[],
        )
    )
    assert result is not None


def test_delete_an_assignment():
    result = delete_an_assignment(entity_id="3a7cf5fc-6554-4136-918b-6f494656b2b0", resource_id="71fe66b9-b3ea-4fc7-8594-541d0a07a697")
    assert result is True


# def test_retrieve_an_assignment():
#     result = retrieve_an_assignment(entity_id: str, resource_id: str)
#     assert result is not None


# def test_update_assignment_roles():
#     result = update_assignment_roles(request_body: EntityRolesRequest, entity_id: str, resource_id: str)
#     assert result is not None


# def test_retrieve_resource_assignments():
#     result = retrieve_resource_assignments(resource_ids: str)
#     assert result is not None


# def test_create_multiple_assignments():
#     result = create_multiple_assignments(request_body: MultipleAssignmentInput)
#     assert result is not None


# def test_add_roles_to_assignment():
#     result = add_roles_to_assignment(request_body: AddAssignmentRoles)
#     assert result is not None


def test_retrieve_entities():
    resource_id = "1b49ad6f-057f-400c-aa32-f6bc31caf242"
    resource_type = ResourceType.PROJECT
    result = retrieve_entities(resource_id=resource_id, resource_type=resource_type, entity_types=None)
    print(f"result: {result}")
    assert len(result) == 2


# def test_retrieve_extended_entities_for_resource():
#     result = retrieve_extended_entities_for_resource(resource_id: str, resource_type: str, entity_types: str = None, sort_by: str = None, order: str = None, limit: None = None, offset: None = None, search: str = None)
#     assert result is not None


# def test_retrieve_resources():
#     result = retrieve_resources(entity_id: str, resource_types: str = None)
#     assert result is not None


def test_check_access():
    resource_id = "71fe66b9-b3ea-4fc7-8594-541d0a07a697"
    resource_type = ResourceType.TENANTGROUP
    action = "create-project"
    result = check_access(resource_id=resource_id, resource_type=resource_type, action=action)
    assert result is not None


# def test_check_access_to_requested_groups():
#     result = check_access_to_requested_groups(group_ids: List[str], project_id: str = None)
#     assert result is not None


# def test_retrieve_accessible_resources():
#     result = retrieve_accessible_resources(resource_types: str, action: str)
#     assert result is not None


# def test_retrieve_user's_or_client_groups():
#     result = retrieve_user's_or_client_groups(include_subgroups: bool = None, search: str = None, limit: None = None, offset: None = None)
#     assert result is not None


# def test_retrieve_user's_or_client_available_groups():
#     result = retrieve_user's_or_client_available_groups(project_id: bool = None, search: str = None, limit: None = None, offset: None = None)
#     assert result is not None


# def test_retrieve_groups():
#     result = retrieve_groups(limit: None = None, offset: None = None, search: str = None, ids: str = None)
#     assert result is not None


# def test_retrieve_users():
#     result = retrieve_users(limit: None = None, offset: None = None, search: None = None)
#     assert result is not None


# def test_retrieve_clients():
#     result = retrieve_clients()
#     assert result is not None


# def test_retrieve_users_from_internal_am_storage():
#     result = retrieve_users_from_internal_am_storage()
#     assert result is not None


# def test_retrieve_groups_from_internal_am_storage():
#     result = retrieve_groups_from_internal_am_storage()
#     assert result is not None


# def test_retrieve_clients_from_internal_am_storage():
#     result = retrieve_clients_from_internal_am_storage()
#     assert result is not None


# def test_retrieve_entity's_base_roles():
#     result = retrieve_entity's_base_roles(entity_id: str)
#     assert result is not None


# def test_update_base_roles_for_an_entity():
#     result = update_base_roles_for_an_entity(request_body: BaseRolesRequest, entity_id: str)
#     assert result is not None


# def test_assign_base_roles_to_an_entity():
#     result = assign_base_roles_to_an_entity(request_body: BaseRolesRequest, entity_id: str)
#     assert result is not None


# def test_delete_base_roles_for_an_entity():
#     result = delete_base_roles_for_an_entity(entity_id: str)
#     assert result is not None


# def test_assign_base_roles_by_role_name():
#     result = assign_base_roles_by_role_name(request_body: BaseRolesRequest, entity_id: str)
#     assert result is not None


# def test_unassign_base_roles_by_role_name():
#     result = unassign_base_roles_by_role_name(request_body: BaseRolesRequest, entity_id: str)
#     assert result is not None


# def test_retrieve_roles():
#     result = retrieve_roles()
#     assert result is not None


# def test_create_a_role():
#     result = create_a_role(request_body: CreateRoleRequest)
#     assert result is not None


# def test_retrieve_role():
#     result = retrieve_role(role_id: str)
#     assert result is not None


# def test_update_a_role():
#     result = update_a_role(request_body: CreateRoleRequest, role_id: str)
#     assert result is not None


# def test_delete_a_role():
#     result = delete_a_role(role_id: str)
#     assert result is not None


# def test_retrieve_permissions():
#     result = retrieve_permissions()
#     assert result is not None


# def test_retrieve_users_with_resources():
#     result = retrieve_users_with_resources(search: str = None, base_roles: str = None, username: str = None, empty_assignments: bool = None, no_groups: bool = None, created_from: str = None, created_to: str = None, sort_by: str = None, order: str = None, limit: None = None, offset: None = None)
#     assert result is not None


# def test_retrieve_clients_with_resources():
#     result = retrieve_clients_with_resources(search: str = None, base_roles: str = None, client_id: str = None, empty_assignments: bool = None, sort_by: str = None, order: str = None, limit: None = None, offset: None = None, no_groups: bool = None, created_from: str = None, created_to: str = None)
#     assert result is not None


# def test_retrieve_groups_with_resources():
#     result = retrieve_groups_with_resources(search: str = None, base_roles: str = None, name: str = None, empty_assignments: bool = None, no_members: bool = None, sort_by: str = None, created_from: str = None, created_to: str = None, order: str = None, limit: None = None, offset: None = None)
#     assert result is not None


# def test_get_a_list_of_permissions_of_entity_for_resource():
#     result = get_a_list_of_permissions_of_entity_for_resource(entity_id: str, entity_type: str, resource_id: str = None, resource_type: str)
#     assert result is not None


# def test_get_a_list_of_applications_with_action_for_user/client():
#     result = get_a_list_of_applications_with_action_for_user/client(action: str, offset: int = None, limit: int = None, name: str = None, tags_keys: List[str] = None, tags_values: List[str] = None)
#     assert result is not None


# def test_get_a_list_of_projects_with_action_for_user/client():
#     result = get_a_list_of_projects_with_action_for_user/client(action: str, offset: int = None, limit: int = None, name: str = None, tags_keys: List[str] = None, tags_values: List[str] = None)
#     assert result is not None

