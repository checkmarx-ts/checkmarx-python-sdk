from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED, OK
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    AssignmentInput,
    AssignmentsForResource, construct_assignments_for_resource,
    Assignment, construct_assignment,
    MultipleAssignmentInput,
    AddAssignmentRoles,
    ResourcesResponse, construct_resources_response,
    UsersWithResourcesResponse, construct_users_with_resources_response,
    ClientsWithResourcesResponse, construct_clients_with_resources_response,
    GroupsWithResourcesResponse, construct_groups_with_resources_response,
    BaseRolesResponse, construct_base_roles_response,
    BaseRolesRequest,
    RoleWithDetails, construct_role_with_details,
    Permission, construct_permission,
    EntityRolesRequest,
    CreateRoleRequest,
    GroupsResponse, construct_groups_response,
    Group, construct_group,
    User, construct_user,
    Client, construct_client,
    construct_internal_user,
    construct_internal_group,
    InternalClient, construct_internal_client,
    EffectivePermissionsForResourceResponse, construct_effective_permissions_for_resource_response,
    EntitiesForExtendedResponse, construct_entities_for_extended_response,
    ApplicationsCollection, construct_applications_collection,
    ProjectsCollection, construct_projects_collection,
    EntityType, ResourceType,
)

api_url = "/api/access-management"


class AccessManagementAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_an_assignment(self, assignment_input: AssignmentInput) -> bool:
        """
        Use this API to create an "assignment". An "assignment" specifies one or more "entities" (user, group, or OAuth
        Client) and grants them permission to access specific "resources" (tenant, application or project). You can also
        specify "roles" that designate the permissions for this assignment. If not specified, the tenant wide permission
        for each user is applied. The request body is a JSON object that defines all of relevant parameters for the
        assignment.
        """
        relative_url = f"{api_url}/"
        response = self.api_client.post_request(relative_url=relative_url, json=assignment_input.to_dict())
        return response.status_code == CREATED

    def delete_an_assignment(self, entity_id: str, resource_id: str) -> bool:
        """
        Delete an assignment. This revokes all permissions associated with the assignment.
        Args:
            entity_id (str): The unique identifier of the entity (user, group or client) for which the assignment will
                             be deleted.
            resource_id (str): The unique identifier of the resource (tenant, application or project) for which the
                             assignment will be deleted.

        Returns:
            bool
        """
        relative_url = f"{api_url}/"
        params = {"entity-id": entity_id, "resource-id": resource_id}
        response = self.api_client.delete_request(relative_url=relative_url, params=params)
        return response.status_code == OK

    def retrieve_an_assignment(self, entity_id: str, resource_id: str) -> Assignment:
        """
        Get detailed information about a specific assignment.
        Args:
            entity_id (str): The unique identifier of the entity (user, group or client)
            resource_id (str): The unique identifier of the resource (tenant, application or project)

        Returns:
            Assignment
        """
        relative_url = f"{api_url}/"
        params = {"entity-id": entity_id, "resource-id": resource_id}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_assignment(response.json())

    def update_assignment_roles(self, entity_roles: EntityRolesRequest, entity_id: str, resource_id: str) -> bool:
        """
        Update the roles assigned to the entity for the specified assignment.
        Args:
            entity_roles (EntityRolesRequest): Specify the new roles that will be assigned to the entity for this
                                                assignment
            entity_id (str): The unique identifier of the entity (user, group or client) that is being updated
            resource_id (str): The unique identifier of the resource (tenant, application or project)

        Returns:
            bool
        """
        relative_url = f"{api_url}/"
        params = {"entity-id": entity_id, "resource-id": resource_id}
        response = self.api_client.put_request(relative_url=relative_url, params=params, json=entity_roles.to_dict())
        return response.status_code == OK

    def retrieve_resource_assignments(self, resource_ids: List[str]) -> AssignmentsForResource:
        """
        Retrieves detailed information about each assignment that exists for specific resources.
        Args:
            resource_ids (List[str]): The unique identifiers of one or more resources (comma separated)

        Returns:
            AssignmentsForResource
        """
        relative_url = f"{api_url}/resource-assignments"
        params = {"resource-ids": ",".join(resource_ids) if resource_ids else None}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_assignments_for_resource(response.json())

    def create_multiple_assignments(self, multiple_assignment: MultipleAssignmentInput) -> bool:
        """
        Use this API to create multiple assignments with one action. Specify one or more "entities" (user, usergroup, or
        OAuth Client) and one or more "resources" (tenant, application or project) to which they are given access. Also,
        specify the "roles" that designate the permissions for all assignments created with this action. If not
        specified, then the default "base" role is applied for each entity. The request body is a JSON object that
        defines all relevant parameters for the assignments.

        Args:
            multiple_assignment (MultipleAssignmentInput):

        Returns:
            bool
        """
        relative_url = f"{api_url}/assignments"
        response = self.api_client.post_request(relative_url=relative_url, json=multiple_assignment.to_dict())
        return response.status_code == CREATED

    def add_roles_to_assignment(self, assignment_roles: AddAssignmentRoles) -> bool:
        """
        Add roles to an existing assignment
        Args:
            assignment_roles (AddAssignmentRoles):

        Returns:
            bool
        """
        relative_url = f"{api_url}/assignments/roles"
        response = self.api_client.post_request(relative_url=relative_url, json=assignment_roles.to_dict())
        return response.status_code == OK

    def retrieve_entities(
            self, resource_id: str, resource_type: ResourceType, entity_types: List[EntityType] = None
    ) -> Assignment:
        """
        Get a list of entities that are assigned to a specific resource
        Args:
            resource_id (str): The unique identifier of the resource
            resource_type (ResourceType): The type of resource (tenant, application or project)
            entity_types (List[EntityType]): Comma separate list of entity types (user, group or client) to return.
                                            Default: Returns all entities. present.

        Returns:
            Assignment
        """
        relative_url = f"{api_url}/entities-for"
        params = {"resource-id": resource_id, "resource-type": resource_type,
                  "entity-types": ",".join(entity_types) if entity_types else None}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_assignment(response.json())

    def retrieve_extended_entities_for_resource(
            self, resource_id: str, resource_type: ResourceType, entity_types: List[EntityType] = None,
            sort_by: str = "entity_name", order: str = "asc", limit: int = 10, offset: int = 0, search: str = None
    ) -> EntitiesForExtendedResponse:
        """
        Get a list of more detailed information about the entities assigned to the resource.
        Args:
            resource_id (str): The unique identifier of the resource
            resource_type (ResourceType): The type of resource (tenant, application or project) Example : project
            entity_types (List[EntityType]): Comma separate list of entity types (user, group or client) to return.
                                             Default: Returns all entities. present. Example : user,group
            sort_by (str): Field for sorting the data Available values : entity_name
            order (str): Order records by username Available values : asc, desc Default value : asc
            limit (int): Max number of records Default value : 10
            offset (int): Start from Default value : 0
            search (str): Search by entity name

        Returns:
            EntitiesForExtendedResponse
        """
        relative_url = f"{api_url}/entities-for/extended"
        params = {
            "resource-id": resource_id, "resource-type": resource_type,
            "entity-types": ",".join(entity_types) if entity_types else None,
            "sort-by": sort_by, "order": order, "limit": limit, "offset": offset, "search": search
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_entities_for_extended_response(response.json())

    def retrieve_resources(self, entity_id: str, resource_types: List[ResourceType] = None) -> List[Assignment]:
        """
        Get a list of resources to which a specific entity is assigned
        Args:
            entity_id (str): The unique identifier of the entity (user, group or client)
            resource_types (List[ResourceType]): Comma separated list of resource types for which results will be
                                                 returned. Default: Results are returned for all types of resources.
                                                 Example : project,tenant

        Returns:
            List[Assignment]
        """
        relative_url = f"{api_url}/resources-for"
        params = {"entity-id": entity_id, "resource-types": ",".join(resource_types) if resource_types else None}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return [construct_assignment(assignment) for assignment in response.json()]

    def check_access(self, resource_id: str, resource_type: ResourceType, action: str) -> bool:
        """
        Check if the current user (as identified by JWT token) has permission to do a particular action on a particular
        resource.
        Args:
            resource_id (str): The unique identifier of the resource
            resource_type (ResourceType): The type of resource. The 'tenantgroup' - to check tenant level assignment;
                                 'application' - to check assignment to application; 'project' - to check assignment to
                                 project; 'tenant' or 'global' - to  check access though base role. Available values :
                                 application, project, tenantgroup, tenant, global  Example : project
            action (str): The action for which you are checking if permission is granted. You can submit any of the
                          Action Roles listed here.

        Returns:
            bool
        """
        relative_url = f"{api_url}/has-access"
        params = {"resource-id": resource_id, "resource-type": resource_type, "action": action}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return response.status_code == OK

    def check_access_to_requested_groups(self, group_ids: List[str], project_id: str = None) -> bool:
        """

        Args:
            group_ids (List[str]): The list of unique identifiers of groups (with coma separator)
            project_id (str): The unique identifier of project. If provided it checks at Project level otherwise on
                              Tenant Level

        Returns:
            bool
        """
        relative_url = f"{api_url}/has-access-to-groups"
        params = {"group-ids": ",".join(group_ids) if group_ids else None, "project-id": project_id}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return response.status_code == OK

    def retrieve_accessible_resources(self, resource_types: List[ResourceType], action: str) -> ResourcesResponse:
        """
        Get a list of resources that are assigned to the current user (as identified by JWT token).
        Args:
            resource_types (List[ResourceType]): The type of resource for which you are retrieving a list of accessible
                                        resources
                                        Multiple types can be submitted (comma separated).
                                        The 'tenantgroup' - to check tenant level assignment;
                                        'application' - to check assignment to application;
                                        'project' - to check assignment to project;
                                        'tenant' or 'global' - to check access though base role.
                                        Available values : application, project, tenantgroup, tenant, global
                                        Example : project,application
            action (str): The action for which you are checking for accessible resources. You can submit any of the
                          Action Roles listed here.
        Returns:
            ResourcesResponse
        """
        relative_url = f"{api_url}/get-resources"
        params = {"resource-types": ",".join(resource_types) if resource_types else None, "action": action}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_resources_response(response.json())

    def retrieve_users_with_resources(
            self, search: str = None, base_roles: List[str] = None, usernames: List[str] = None,
            empty_assignments: bool = None, no_groups: bool = None, created_from: str = None, created_to: str = None,
            sort_by: str = "created-at", order: str = 'asc', limit: int = None, offset: int = None
    ) -> UsersWithResourcesResponse:
        """

        Args:
            search (str): Search by username, firstName, lastName. Returns results that start with the search
            base_roles (List[str]): Filter by base roles, separated with a comma (filter by one role or another).
                                   Example : ast-admin,manage-roles
            usernames (List[str]): Filter by usernames, separated with a comma (filter by one username or another).
                                    Example : username1,username2
            empty_assignments (bool): Filter by assignments. Example : true
            no_groups (bool): Filter users by group membership. Set to "true" to show only users without
                              groups, "false" to show only users with groups. If not set, all users will be returned.
            created_from (str): Filter users by creation date. Use to specify the start date. Date format
                                YYYY-MM-DDTHH:mm:ss Example : 2025-01-31T12:00:00
            created_to (str): Filter users by creation date. Use to specify the end date. Date format
                                YYYY-MM-DDTHH:mm:ss Example : 2025-01-31T12:00:00
            sort_by (str): Field for sorting the data Available values : created-at, username Default value : created-at
            order (str): Order records by username Available values : asc, desc Default value : asc
            limit (int): Max number of records
            offset (int): Start from

        Returns:
            MessageQueuePassword
        """
        """Get a list of users with the resources assigned to each user."""
        relative_url = f"{api_url}/users-resources"
        params = {
            "search": search, "base-roles": ",".join(base_roles) if base_roles else None,
            "username": ",".join(usernames) if usernames else None,
            "empty-assignments": empty_assignments, "no-groups": no_groups, "created-from": created_from,
            "created-to": created_to, "sort-by": sort_by, "order": order, "limit": limit, "offset": offset
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_users_with_resources_response(response.json())

    def retrieve_clients_with_resources(
            self, search: str = None, base_roles: List[str] = None, client_ids: List[str] = None,
            empty_assignments: bool = True, sort_by: str = "created-at", order: str = "asc", limit: int = None,
            offset: int = None, no_groups: bool = True, created_from: str = None, created_to: str = None
    ) -> ClientsWithResourcesResponse:
        """
        Get a list of clients and the resources assigned to each client.
        Args:
            search (str): Search the clients which client-id starts with the search value
            base_roles (List[str]): Filter by base roles, separated with a comma (filter by one role or another).
                                    Example : ast-admin,manage-roles
            client_ids (List[str]): Filter by values of client-id, separated with a comma (filter by one client-id or
                                    another). Example : client1,client2
            empty_assignments (bool): Filter by assignments. Example : true
            sort_by (str): Field for sorting the data Available values : created-at, client-id Default value: created-at
            order (str): Order records by client-id Available values : asc, desc Default value : asc
            limit (int): The maximum number of results to return
            offset (int): The number of pages to skip before starting to return results.
                          The number of results per page is defined by the value of limit.
            no_groups (bool): Filter clients by group membership. Set to "true" to show only clients without groups,
                            "false" to show only clients with groups. If not set, all clients will be returned.
            created_from (str): Filter clients by creation date. Use to specify the start date. Date format
                              YYYY-MM-DDTHH:mm:ss Example : 2025-01-31T12:00:00
            created_to (str): Filter clients by creation date. Use to specify the start date. Date format
                              YYYY-MM-DDTHH:mm:ss Example : 2025-01-31T12:00:00

        Returns:
            ClientsWithResourcesResponse
        """
        relative_url = f"{api_url}/clients-resources"
        params = {
            "search": search, "base-roles": ",".join(base_roles) if base_roles else None,
            "client-id": ",".join(client_ids) if client_ids else None,
            "empty-assignments": empty_assignments, "sort-by": sort_by, "order": order,
            "limit": limit, "offset": offset, "no-groups": no_groups, "created-from": created_from,
            "created-to": created_to
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_clients_with_resources_response(response.json())

    def retrieve_groups_with_resources(
            self, search: str = None, base_roles: List[str] = None, names: List[str] = None,
            empty_assignments: bool = True, no_members: bool = None, sort_by: str = "created-at",
            created_from: str = None, created_to: str = None, order: str = "asc", limit: int = None, offset: int = None
    ) -> GroupsWithResourcesResponse:
        """
        Get a list of groups with resources assigned to each group.
        Args:
            search (str):  Search the groups which names starts with the search value
            base_roles (List[str]):  Filter by base roles, separated with a comma (filter by one role or another).
                                     Example : ast-admin,manage-roles
            names (List[str]):  Filter by values of name, separated with a comma (filter by one name or another).
                               Example : name1,name2
            empty_assignments (bool):  Filter by assignments. Example : true
            no_members (bool): Filter groups by user/client membership. Set to "true" to show only groups
                              without members, "false" to show only groups with members. If not set, all groups will be
                              returned. Example : true
            sort_by (str): Field for sorting the data Available values : created-at, name Default value : created-at
            created_from (str): Filter clients by creation date. Use to specify the start date. Date format
                                 YYYY-MM-DDTHH:mm:ss Example : 2025-01-31T12:00:00
            created_to (str): Filter clients by creation date. Use to specify the end date. Date format
                                YYYY-MM-DDTHH:mm:ss Example : 2025-01-31T12:00:00
            order (str):  Order records by group name Available values : asc, desc Default value : asc
            limit (int): Max number of records
            offset (int): Start from

        Returns:
            GroupsWithResourcesResponse
        """
        relative_url = f"{api_url}/groups-resources"
        params = {
            "search": search, "base-roles": ",".join(base_roles) if base_roles else None,
            "name": ",".join(names) if names else None, "empty-assignments": empty_assignments,
            "no-members": no_members, "sort-by": sort_by, "created-from": created_from, "created-to": created_to,
            "order": order, "limit": limit, "offset": offset
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_groups_with_resources_response(response.json())

    def get_a_list_of_permissions_of_entity_for_resource(
            self, entity_id: str, entity_type: EntityType, resource_id: str = None, resource_type: ResourceType = None
    ) -> EffectivePermissionsForResourceResponse:
        """
        Get a list of permissions of an entity (user, client, group) for a specific resource (project, program,
        tenant group, global/tenant) without specifying where they were assigned from
        Args:
            entity_id (str):
            entity_type (EntityType): The type of entity Available values : user, client, group Example : user
            resource_id (str): The unique identifier of the resource. Not required if resource-type is tenant/global.
            resource_type (ResourceType): The type of resource Available values : project, application, tenantgroup,
                                 tenant, global Example : project

        Returns:
            EffectivePermissionsForResourceResponse
        """
        relative_url = f"{api_url}/effective-permissions/{entity_id}"
        params = {
            "entity-type": entity_type, "resource-id": resource_id, "resource-type": resource_type
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_effective_permissions_for_resource_response(response.json())

    def get_a_list_of_applications_with_action_for_user_or_client(
            self, action: str, offset: int = 0, limit: int = 20, name: str = None, tags_keys: List[str] = None,
            tags_values: List[str] = None
    ) -> ApplicationsCollection:
        """
        Get a list of applications for an entity (user, client) with a specific action (permission).
        Args:
            action (str):
            offset (int):  The number of items to skip before starting to collect the result set Default value : 0
            limit (int):  The number of items to return Default value : 20
            name (str):  Application name, can be filtered by partial name.
            tags_keys (List[str]): Application tags, filter by the keys in the tags map (OR operation between the items)
            tags_values (List[str]): Application tags, filter by the values in the tags map (OR operation between the
                                    items)

        Returns:
            ApplicationsCollection
        """
        relative_url = f"{api_url}/applications"
        params = {
            "action": action, "offset": offset, "limit": limit, "name": name, "tags-keys": tags_keys,
            "tags-values": tags_values
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_applications_collection(response.json())

    def get_a_list_of_projects_with_action_for_user_or_client(
            self, action: str, offset: int = 0, limit: int = 20, name: str = None, tags_keys: List[str] = None,
            tags_values: List[str] = None
    ) -> ProjectsCollection:
        """
        Get a list of projects for an entity (user, client) with a specific action (permission).
        Args:
            action (str):
            offset (int):  The number of items to skip before starting to collect the result set Default value : 0
            limit (int):  The number of items to return Default value : 20
            name (str): Project name, can be filtered by partial name. Mutually exclusive to names and name-regex
            tags_keys (List[str]): Project tags, filter by the keys in the tags map (OR operation between the items)
            tags_values (List[str]): Project tags, filter by the values in the tags map (OR operation between the items)

        Returns:
            ProjectsCollection
        """
        relative_url = f"{api_url}/projects"
        params = {
            "action": action, "offset": offset, "limit": limit, "name": name, "tags-keys": tags_keys,
            "tags-values": tags_values
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_projects_collection(response.json())

    def retrieve_user_or_client_groups(
            self, include_subgroups: bool = False, search: str = None, limit: int = None, offset: int = None
    ) -> GroupsResponse:
        """
        Get a list of user/client groups to which the current user (as identified by JWT token) is assigned. Search
        for clients groups only available for phase 2.
        Args:
            include_subgroups (bool): Set param to 'true' to include subgroups in the response Default value : false
            search (str):  Search by group name
            limit (int):  The maximum number of results to return
            offset (int): The number of pages to skip before starting to return results. The number of results per page
                         is defined by the value of limit.

        Returns:
            GroupsResponse
        """
        relative_url = f"{api_url}/my-groups"
        params = {"include-subgroups": include_subgroups, "search": search, "limit": limit, "offset": offset}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_groups_response(response.json())

    def retrieve_user_or_client_available_groups(
            self, project_id: str = None, search: str = None, limit: int = None, offset: int = None
    ) -> GroupsResponse:
        """
        Get a list of groups available for user/client on project/global level.
        Args:
            project_id (str): The unique identifier of the project. If not provided, check access on tenant level.
                              Default value : false
            search (str): Search by group name
            limit (int): The maximum number of results to return
            offset (int): The number of pages to skip before starting to return results. The number of results
                        per page is defined by the value of limit.
        Returns:
            GroupsResponse
        """
        relative_url = f"{api_url}/available-groups"
        params = {"project-id": project_id, "search": search, "limit": limit, "offset": offset}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_groups_response(response.json())

    def retrieve_groups(
            self, limit: int = None, offset: int = None, search: str = None, ids: List[str] = ()
    ) -> List[Group]:
        """
        Get info about user groups in the tenant account
        Args:
            limit (int): The maximum number of results to return
            offset (int): The number of pages to skip before starting to return results. The number of results
                          per page is defined by the value of limit.
            search (str): Search by group name
            ids (List[str]):  Filter by group IDs (comma separated)

        Returns:
            List[Group]
        """
        relative_url = f"{api_url}/groups"
        params = {"limit": limit, "offset": offset, "search": search, "ids": ",".join(ids)}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return [construct_group(group) for group in response.json()]

    def retrieve_users(
            self, limit: int = None, offset: int = None, search: str = None
    ) -> List[User]:
        """
        Get info about users in the tenant account.
        Args:
            limit (int): The maximum number of results to return
            offset (int): The number of pages to skip before starting to return results. The number of results
                         per page is defined by the value of limit.
            search (str): Search by username, firstname, lastname or email

        Returns:
            List[User]
        """
        relative_url = f"{api_url}/users"
        params = {"limit": limit, "offset": offset, "search": search}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return [construct_user(user) for user in response.json()]

    def retrieve_clients(self) -> List[Client]:
        """
        Get info about OAuth clients in the tenant account
        Returns:
            List[Client]:
        """
        relative_url = f"{api_url}/clients"
        response = self.api_client.get_request(relative_url=relative_url)
        return [construct_client(client) for client in response.json()]

    def retrieve_users_from_internal_am_storage(self) -> dict:
        """

        Get info about users in the tenant account.
        This returns the same info as /users, but it gets results more quickly because it draws the info from our
        internal Access Management database.

        Returns:
            dict
        """
        relative_url = f"{api_url}/internal/users"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return {
            "total": item.get("total"),
            "users": [
                construct_internal_user(user) for user in item.get("users")
            ]
        }

    def retrieve_groups_from_internal_am_storage(self) -> dict:
        """
        Get info about OAuth clients in the tenant account.
        This returns the same info as /clients, but it gets results more quickly because it draws the info from our
        internal Access Management database.

        Returns:
            dict
        """
        relative_url = f"{api_url}/internal/groups"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return {
            "total": item.get("total"),
            "groups": [
                construct_internal_group(group) for group in item.get("groups")
            ]
        }

    def retrieve_clients_from_internal_am_storage(self) -> List[InternalClient]:
        """
        Get AM clients

        Returns:
             List[InternalClient]
        """
        relative_url = f"{api_url}/internal/clients"
        response = self.api_client.get_request(relative_url=relative_url)
        return [construct_internal_client(client) for client in response.json()]

    def retrieve_entity_base_roles(self, entity_id: str) -> BaseRolesResponse:
        """
        Get the base roles for a specific entity (user, group or client). 'Base roles' are the set of permissions
        granted to the entity by default for assignments in which no roles were designated.

        Returns:
           BaseRolesResponse
        """
        relative_url = f"{api_url}/base-roles/{entity_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_base_roles_response(response.json())

    def update_base_roles_for_an_entity(self, base_roles: BaseRolesRequest, entity_id: str) -> bool:
        """

        Update the base roles for the specified entity. This will overwrite the existing base roles.
        'Base roles' are the set of permissions granted to the entity by default for assignments in which no roles were
        designated.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
        """
        relative_url = f"{api_url}/base-roles/{entity_id}"
        response = self.api_client.put_request(relative_url=relative_url, json=base_roles.to_dict())
        return response.status_code == OK

    def assign_base_roles_to_an_entity(self, base_roles: BaseRolesRequest, entity_id: str) -> bool:
        """
        Add base roles to the specified entity. If the entity already has base roles, this will add additional roles
         without overwriting the existing roles. The body is an array of role IDs.
        'Base roles' are the set of permissions granted to the entity by default for assignments in which no roles were
         designated.

        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
         """
        relative_url = f"{api_url}/base-roles/{entity_id}"
        response = self.api_client.post_request(relative_url=relative_url, json=base_roles.to_dict())
        return response.status_code == CREATED

    def delete_base_roles_for_an_entity(self, entity_id: str) -> bool:
        """
        Delete the base roles for a specific entity
        Args:
            entity_id (str):

        Returns:
            bool
        """
        relative_url = f"{api_url}/base-roles/{entity_id}"
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT

    def assign_base_roles_by_role_name(self, base_roles: BaseRolesRequest, entity_id: str) -> bool:
        """
        Add base roles to the specified entity. If the entity already has base roles, this will add additional roles
        without overwriting the existing roles. The body is an array of role names.
        'Base roles' are the set of permissions granted to the entity by default for assignments in which no roles were
         designated.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
         """
        relative_url = f"{api_url}/base-roles/{entity_id}/by-name"
        response = self.api_client.post_request(relative_url=relative_url, json=base_roles.to_dict())
        return response.status_code == CREATED

    def unassign_base_roles_by_role_name(self, base_roles: BaseRolesRequest, entity_id: str) -> bool:
        """
        Revoke base roles from an entity by specifying the role names.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
        """
        relative_url = f"{api_url}/base-roles/{entity_id}/by-name/unassign"
        response = self.api_client.post_request(relative_url=relative_url, json=base_roles.to_dict())
        return response.status_code == CREATED

    def retrieve_roles(self) -> List[RoleWithDetails]:
        """
        Get info about roles in the tenant account.

        Returns:
            List[RoleWithDetails]:
        """
        relative_url = f"{api_url}/roles"
        response = self.api_client.get_request(relative_url=relative_url)
        return [construct_role_with_details(role) for role in response.json()]

    def create_a_role(self, role_request: CreateRoleRequest) -> bool:
        """
         Creates a new role, specifying the series of permissions that are assigned to the new role. Roles can then
         be assigned to entities (user, group or client) in the context of assignment creation.
         The request body is a JSON object that defines all relevant parameters for the role.
         Note: You can obtain a complete list of available permissions using GET /permissions

        Returns:
            bool
        """
        relative_url = f"{api_url}/roles"
        response = self.api_client.post_request(relative_url=relative_url, json=role_request.to_dict())
        return response.status_code == CREATED

    def retrieve_role(self, role_id: str) -> RoleWithDetails:
        """
        Get information about a specific role, specified by roleId.
        Args:
            role_id (str):

        Returns:
            RoleWithDetails
        """
        relative_url = f"{api_url}/roles/{role_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_role_with_details(response.json())

    def update_a_role(self, role_request: CreateRoleRequest, role_id: str) -> bool:
        """
        Edit the configuration of an existing role. The body content is the same as for the POST method.
        Note: All parameters are overwritten by the new configuration. If you would like to add permissions to a role,
        you need to submit all current permissions as well as the new permissions that are being added.
        Note: System roles (out-of-the-box) cannot be updated.

        Args:
            role_request (CreateRoleRequest):
            role_id (str):

        Returns:
            bool
        """
        relative_url = f"{api_url}/roles/{role_id}"
        response = self.api_client.put_request(relative_url=relative_url, json=role_request.to_dict())
        return response.status_code == CREATED

    def delete_a_role(self, role_id: str) -> bool:
        """
        Deletes a role.
            Note: System roles (out-of-the-box cannot be deleted).
        Args:
            role_id (str):

        Returns:
            bool
            """
        relative_url = f"{api_url}/roles/{role_id}"
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == OK

    def retrieve_permissions(self) -> List[Permission]:
        """
        Get info about all permissions that are available in the system.

        Returns:
            List[Permission]
        """
        relative_url = f"{api_url}/permissions"
        response = self.api_client.get_request(relative_url=relative_url)
        return [construct_permission(permission) for permission in response.json()]


def create_an_assignment(assignment_input: AssignmentInput) -> bool:
    return AccessManagementAPI().create_an_assignment(assignment_input=assignment_input)


def delete_an_assignment(entity_id: str, resource_id: str) -> bool:
    return AccessManagementAPI().delete_an_assignment(entity_id=entity_id, resource_id=resource_id)


def retrieve_an_assignment(entity_id: str, resource_id: str) -> Assignment:
    return AccessManagementAPI().retrieve_an_assignment(entity_id=entity_id, resource_id=resource_id)


def update_assignment_roles(entity_roles: EntityRolesRequest, entity_id: str, resource_id: str) -> bool:
    return AccessManagementAPI().update_assignment_roles(
        entity_roles=entity_roles, entity_id=entity_id, resource_id=resource_id
    )


def retrieve_resource_assignments(resource_ids: List[str]) -> AssignmentsForResource:
    return AccessManagementAPI().retrieve_resource_assignments(resource_ids=resource_ids)


def create_multiple_assignments(multiple_assignment: MultipleAssignmentInput) -> bool:
    return AccessManagementAPI().create_multiple_assignments(multiple_assignment=multiple_assignment)


def add_roles_to_assignment(assignment_roles: AddAssignmentRoles) -> bool:
    return AccessManagementAPI().add_roles_to_assignment(assignment_roles=assignment_roles)


def retrieve_entities(
        resource_id: str, resource_type: ResourceType, entity_types: List[EntityType] = None
) -> Assignment:
    return AccessManagementAPI().retrieve_entities(
        resource_id=resource_id, resource_type=resource_type, entity_types=entity_types
    )


def retrieve_extended_entities_for_resource(
        resource_id: str, resource_type: ResourceType, entity_types: List[EntityType] = None,
        sort_by: str = "entity_name", order: str = "asc", limit: int = 10, offset: int = 0, search: str = None
) -> EntitiesForExtendedResponse:
    return AccessManagementAPI().retrieve_extended_entities_for_resource(
        resource_id=resource_id, resource_type=resource_type, entity_types=entity_types, sort_by=sort_by,
        order=order, limit=limit, offset=offset, search=search
    )


def retrieve_resources(entity_id: str, resource_types: List[ResourceType] = None) -> List[Assignment]:
    return AccessManagementAPI().retrieve_resources(entity_id=entity_id, resource_types=resource_types)


def check_access(resource_id: str, resource_type: ResourceType, action: str) -> bool:
    return AccessManagementAPI().check_access(resource_id=resource_id, resource_type=resource_type, action=action)


def check_access_to_requested_groups(group_ids: List[str], project_id: str = None) -> bool:
    return AccessManagementAPI().check_access_to_requested_groups(group_ids=group_ids, project_id=project_id)


def retrieve_accessible_resources(resource_types: List[ResourceType], action: str) -> ResourcesResponse:
    return AccessManagementAPI().retrieve_accessible_resources(resource_types=resource_types, action=action)


def retrieve_users_with_resources(
        search: str = None, base_roles: List[str] = None, usernames: List[str] = None, empty_assignments: bool = None,
        no_groups: bool = None, created_from: str = None, created_to: str = None, sort_by: str = "created-at",
        order: str = 'asc', limit: int = None, offset: int = None
) -> UsersWithResourcesResponse:
    return AccessManagementAPI().retrieve_users_with_resources(
        search=search, base_roles=base_roles, usernames=usernames, empty_assignments=empty_assignments,
        no_groups=no_groups, created_from=created_from, created_to=created_to, sort_by=sort_by, order=order,
        limit=limit, offset=offset
    )


def retrieve_clients_with_resources(
        search: str = None, base_roles: str = None, client_ids: List[str] = None, empty_assignments: bool = None,
        sort_by: str = "created-at", order: str = "asc", limit: int = None, offset: int = None, no_groups: bool = None,
        created_from: str = None, created_to: str = None
) -> ClientsWithResourcesResponse:
    return AccessManagementAPI().retrieve_clients_with_resources(
        search=search, base_roles=base_roles, client_ids=client_ids, empty_assignments=empty_assignments,
        sort_by=sort_by, order=order, limit=limit, offset=offset, no_groups=no_groups, created_from=created_from,
        created_to=created_to
    )


def retrieve_groups_with_resources(
        search: str = None, base_roles: str = None, names: List[str] = None, empty_assignments: bool = True,
        no_members: bool = True, sort_by: str = "created-at", created_from: str = None, created_to: str = None,
        order: str = "asc", limit: int = None, offset: int = None
) -> GroupsWithResourcesResponse:
    return AccessManagementAPI().retrieve_groups_with_resources(
        search=search, base_roles=base_roles, names=names, empty_assignments=empty_assignments, no_members=no_members,
        sort_by=sort_by, created_from=created_from, created_to=created_to, order=order, limit=limit, offset=offset,
    )


def get_a_list_of_permissions_of_entity_for_resource(
        entity_id: str, entity_type: EntityType, resource_id: str = None, resource_type: ResourceType = None
) -> EffectivePermissionsForResourceResponse:
    return AccessManagementAPI().get_a_list_of_permissions_of_entity_for_resource(
        entity_id=entity_id, entity_type=entity_type, resource_id=resource_id, resource_type=resource_type,
    )


def get_a_list_of_applications_with_action_for_user_or_client(
        action: str, offset: int = 0, limit: int = 20, name: str = None, tags_keys: List[str] = None,
        tags_values: List[str] = None
) -> ApplicationsCollection:
    return AccessManagementAPI().get_a_list_of_applications_with_action_for_user_or_client(
        action=action, offset=offset, limit=limit, name=name, tags_keys=tags_keys, tags_values=tags_values,
    )


def get_a_list_of_projects_with_action_for_user_or_client(
        action: str, offset: int = 0, limit: int = 20, name: str = None, tags_keys: List[str] = None,
        tags_values: List[str] = None
) -> ProjectsCollection:
    return AccessManagementAPI().get_a_list_of_projects_with_action_for_user_or_client(
        action=action, offset=offset, limit=limit, name=name, tags_keys=tags_keys, tags_values=tags_values,
    )


def retrieve_user_or_client_groups(
        include_subgroups: bool = False, search: str = None, limit: int = None, offset: int = None
) -> GroupsResponse:
    return AccessManagementAPI().retrieve_user_or_client_groups(
        include_subgroups=include_subgroups, search=search, limit=limit, offset=offset,
    )


def retrieve_user_or_client_available_groups(
        project_id: str = None, search: str = None, limit: int = None, offset: int = None
) -> GroupsResponse:
    return AccessManagementAPI().retrieve_user_or_client_available_groups(
        project_id=project_id, search=search, limit=limit, offset=offset,
    )


def retrieve_groups(
        limit: int = None, offset: int = None, search: str = None, ids: List[str] = None
) -> List[Group]:
    return AccessManagementAPI().retrieve_groups(limit=limit, offset=offset, search=search, ids=ids)


def retrieve_users(
        limit: int = None, offset: int = None, search: str = None
) -> List[User]:
    return AccessManagementAPI().retrieve_users(limit=limit, offset=offset, search=search)


def retrieve_clients() -> List[Client]:
    return AccessManagementAPI().retrieve_clients()


def retrieve_users_from_internal_am_storage() -> dict:
    return AccessManagementAPI().retrieve_users_from_internal_am_storage()


def retrieve_groups_from_internal_am_storage() -> dict:
    return AccessManagementAPI().retrieve_groups_from_internal_am_storage()


def retrieve_clients_from_internal_am_storage() -> List[InternalClient]:
    return AccessManagementAPI().retrieve_clients_from_internal_am_storage()


def retrieve_entity_base_roles(entity_id: str) -> BaseRolesResponse:
    return AccessManagementAPI().retrieve_entity_base_roles(entity_id=entity_id)


def update_base_roles_for_an_entity(base_roles: BaseRolesRequest, entity_id: str) -> bool:
    return AccessManagementAPI().update_base_roles_for_an_entity(base_roles=base_roles, entity_id=entity_id)


def assign_base_roles_to_an_entity(base_roles: BaseRolesRequest, entity_id: str) -> bool:
    return AccessManagementAPI().assign_base_roles_to_an_entity(base_roles=base_roles, entity_id=entity_id)


def delete_base_roles_for_an_entity(entity_id: str) -> bool:
    return AccessManagementAPI().delete_base_roles_for_an_entity(entity_id)


def assign_base_roles_by_role_name(base_roles: BaseRolesRequest, entity_id: str) -> bool:
    return AccessManagementAPI().assign_base_roles_by_role_name(base_roles=base_roles, entity_id=entity_id)


def unassign_base_roles_by_role_name(base_roles: BaseRolesRequest, entity_id: str) -> bool:
    return AccessManagementAPI().unassign_base_roles_by_role_name(base_roles=base_roles, entity_id=entity_id)


def retrieve_roles() -> List[RoleWithDetails]:
    return AccessManagementAPI().retrieve_roles()


def create_a_role(role_request: CreateRoleRequest) -> bool:
    return AccessManagementAPI().create_a_role(role_request=role_request)


def retrieve_role(role_id: str) -> RoleWithDetails:
    return AccessManagementAPI().retrieve_role(role_id=role_id)


def update_a_role(role_request: CreateRoleRequest, role_id: str) -> bool:
    return AccessManagementAPI().update_a_role(role_request=role_request, role_id=role_id)


def delete_a_role(role_id: str) -> bool:
    return AccessManagementAPI().delete_a_role(role_id=role_id)


def retrieve_permissions() -> List[Permission]:
    return AccessManagementAPI().retrieve_permissions()
