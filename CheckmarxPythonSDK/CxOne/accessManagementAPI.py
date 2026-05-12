from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED, OK
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    AssignmentInput,
    AssignmentsForResource,
    Assignment,
    MultipleAssignmentInput,
    AddAssignmentRoles,
    ResourcesResponse,
    UsersWithResourcesResponse,
    ClientsWithResourcesResponse,
    GroupsWithResourcesResponse,
    BaseRolesResponse,
    BaseRolesRequest,
    RoleWithDetails,
    Permission,
    EntityRolesRequest,
    CreateRoleRequest,
    GroupsResponse,
    Group,
    User,
    Client,
    InternalUser,
    InternalGroup,
    InternalClient,
    EffectivePermissionsForResourceResponse,
    EntitiesForExtendedResponse,
    ApplicationsCollection,
    ProjectsCollection,
    EntityType,
    ResourceType,
)


class AccessManagementAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/access-management"
        )

    def create_an_assignment(self, assignment_input: AssignmentInput) -> bool:
        """
        Use this API to create an "assignment". An "assignment" specifies
        one or more "entities" (user, group, or OAuth Client) and grants
        them permission to access specific "resources" (tenant, application
        or project). You can also specify "roles" that designate the
        permissions for this assignment. If not specified, the tenant
        wide permission for each user is applied. The request body is a
        JSON object that defines all of relevant parameters for the
        assignment.
        """
        url = self.base_url
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(assignment_input)
        )
        return response.status_code == CREATED

    def delete_an_assignment(self, entity_id: str, resource_id: str) -> bool:
        """
        Delete an assignment. This revokes all permissions associated with
        the assignment.
        Args:
            entity_id (str): The unique identifier of the entity (user,
                group or client) for which the assignment will be deleted.
            resource_id (str): The unique identifier of the resource
                (tenant, application or project) for which the assignment
                will be deleted.

        Returns:
            bool
        """
        url = self.base_url
        params = {"entity-id": entity_id, "resource-id": resource_id}
        response = self.api_client.call_api(method="DELETE", url=url, params=params)
        return response.status_code == OK

    def retrieve_an_assignment(self, entity_id: str, resource_id: str) -> Assignment:
        """
        Get detailed information about a specific assignment.
        Args:
            entity_id (str): The unique identifier of the entity
                (user, group or client)
            resource_id (str): The unique identifier of the resource
                (tenant, application or project)

        Returns:
            Assignment
        """
        url = self.base_url
        params = {"entity-id": entity_id, "resource-id": resource_id}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return Assignment.from_dict(response.json())

    def update_assignment_roles(
        self, entity_roles: EntityRolesRequest, entity_id: str, resource_id: str
    ) -> bool:
        """
        Update the roles assigned to the entity for the specified
        assignment.
        Args:
            entity_roles (EntityRolesRequest): Specify the new roles
                that will be assigned to the entity for this assignment
            entity_id (str): The unique identifier of the entity (user,
                group or client) that is being updated
            resource_id (str): The unique identifier of the resource
                (tenant, application or project)

        Returns:
            bool
        """
        url = self.base_url
        params = {"entity-id": entity_id, "resource-id": resource_id}
        response = self.api_client.call_api(
            method="PUT", url=url, params=params, json=asdict(entity_roles)
        )
        return response.status_code == OK

    def retrieve_resource_assignments(
        self, resource_ids: List[str]
    ) -> AssignmentsForResource:
        """
        Retrieves detailed information about each assignment that exists
        for specific resources.
        Args:
            resource_ids (List[str]): The unique identifiers of one or more
                resources.

        Returns:
            AssignmentsForResource
        """
        url = f"{self.base_url}/resource-assignments"
        params = {"resource-ids": ",".join(resource_ids) if resource_ids else None}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return AssignmentsForResource.from_dict(response.json())

    def create_multiple_assignments(
        self, multiple_assignment: MultipleAssignmentInput
    ) -> bool:
        """
        Use this API to create multiple assignments with one action.
        Specify one or more "entities" (user, usergroup, or OAuth Client)
        and one or more "resources" (tenant, application or project) to
        which they are given access. Also, specify the "roles" that
        designate the permissions for all assignments created with this
        action. If not specified, then the default "base" role is applied
        for each entity.

        Args:
            multiple_assignment (MultipleAssignmentInput):

        Returns:
            bool
        """
        url = f"{self.base_url}/assignments"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(multiple_assignment)
        )
        return response.status_code == CREATED

    def add_roles_to_assignment(self, assignment_roles: AddAssignmentRoles) -> bool:
        """
        Add roles to an existing assignment.
        Args:
            assignment_roles (AddAssignmentRoles):

        Returns:
            bool
        """
        url = f"{self.base_url}/assignments/roles"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(assignment_roles)
        )
        return response.status_code == OK

    def retrieve_entities(
        self,
        resource_id: str,
        resource_type: ResourceType,
        entity_types: List[EntityType] = None,
    ) -> List[Assignment]:
        """
        Get a list of entities that are assigned to a specific resource.
        Args:
            resource_id (str): The unique identifier of the resource
            resource_type (ResourceType): The type of resource (tenant,
                application or project)
            entity_types (List[EntityType]): Comma separate list of entity
                types (user, group or client) to return. Default: Returns
                all entities.

        Returns:
            List[Assignment]
        """
        url = f"{self.base_url}/entities-for"
        params = {
            "resource-id": resource_id,
            "resource-type": resource_type,
            "entity-types": ",".join(entity_types) if entity_types else None,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return [Assignment.from_dict(item) for item in response.json()]

    def retrieve_extended_entities_for_resource(
        self,
        resource_id: str,
        resource_type: ResourceType,
        entity_types: List[EntityType] = None,
        sort_by: str = "entity_name",
        order: str = "asc",
        limit: int = 10,
        offset: int = 0,
        search: str = None,
    ) -> EntitiesForExtendedResponse:
        """
        Get a list of more detailed information about the entities
        assigned to the resource.
        Args:
            resource_id (str): The unique identifier of the resource
            resource_type (ResourceType): The type of resource (tenant,
                application or project)
            entity_types (List[EntityType]): Comma separate list of entity
                types (user, group or client) to return.
            sort_by (str): Field for sorting the data.
                Available values: entity_name
            order (str): Order records by username.
                Available values: asc, desc. Default value: asc
            limit (int): Max number of records. Default value: 10
            offset (int): Start from. Default value: 0
            search (str): Search by entity name

        Returns:
            EntitiesForExtendedResponse
        """
        url = f"{self.base_url}/entities-for/extended"
        params = {
            "resource-id": resource_id,
            "resource-type": resource_type,
            "entity-types": ",".join(entity_types) if entity_types else None,
            "sort-by": sort_by,
            "order": order,
            "limit": limit,
            "offset": offset,
            "search": search,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return EntitiesForExtendedResponse.from_dict(response.json())

    def retrieve_resources(
        self, entity_id: str, resource_types: List[ResourceType] = None
    ) -> List[Assignment]:
        """
        Get a list of resources to which a specific entity is assigned.
        Args:
            entity_id (str): The unique identifier of the entity (user,
                group or client)
            resource_types (List[ResourceType]): Comma separated list of
                resource types for which results will be returned.
                Default: Results are returned for all types of resources.

        Returns:
            List[Assignment]
        """
        url = f"{self.base_url}/resources-for"
        params = {
            "entity-id": entity_id,
            "resource-types": ",".join(resource_types) if resource_types else None,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return [Assignment.from_dict(a) for a in response.json()]

    def check_access(
        self, resource_id: str, resource_type: ResourceType, action: str
    ) -> bool:
        """
        Check if the current user (as identified by JWT token) has
        permission to do a particular action on a particular resource.
        Args:
            resource_id (str): The unique identifier of the resource
            resource_type (ResourceType): The type of resource.
                Available values: application, project, tenantgroup,
                tenant, global
            action (str): The action for which you are checking if
                permission is granted.

        Returns:
            bool
        """
        url = f"{self.base_url}/has-access"
        params = {
            "resource-id": resource_id,
            "resource-type": resource_type,
            "action": action,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return response.json().get("accessGranted") is True

    def check_access_to_requested_groups(
        self, group_ids: List[str], project_id: str = None
    ) -> bool:
        """
        Args:
            group_ids (List[str]): The list of unique identifiers of groups
                (with comma separator)
            project_id (str): The unique identifier of project. If provided
                it checks at Project level otherwise on Tenant Level.

        Returns:
            bool
        """
        url = f"{self.base_url}/has-access-to-groups"
        params = {
            "group-ids": ",".join(group_ids) if group_ids else None,
            "project-id": project_id,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return response.status_code == OK

    def retrieve_accessible_resources(
        self, resource_types: List[ResourceType], action: str
    ) -> ResourcesResponse:
        """
        Get a list of resources that are assigned to the current user
        (as identified by JWT token).
        Args:
            resource_types (List[ResourceType]): The type of resource for
                which you are retrieving a list of accessible resources.
                Multiple types can be submitted (comma separated).
            action (str): The action for which you are checking for
                accessible resources.

        Returns:
            ResourcesResponse
        """
        url = f"{self.base_url}/get-resources"
        params = {
            "resource-types": ",".join(resource_types) if resource_types else None,
            "action": action,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return ResourcesResponse.from_dict(response.json())

    def retrieve_users_with_resources(
        self,
        search: str = None,
        base_roles: List[str] = None,
        usernames: List[str] = None,
        empty_assignments: bool = None,
        no_groups: bool = None,
        created_from: str = None,
        created_to: str = None,
        sort_by: str = "created-at",
        order: str = "asc",
        limit: int = None,
        offset: int = None,
    ) -> UsersWithResourcesResponse:
        """
        Get a list of users with the resources assigned to each user.
        Args:
            search (str): Search by username, firstName, lastName.
            base_roles (List[str]): Filter by base roles (comma separated).
            usernames (List[str]): Filter by usernames (comma separated).
            empty_assignments (bool): Filter by assignments.
            no_groups (bool): Filter users by group membership.
            created_from (str): Filter by creation start date
                (YYYY-MM-DDTHH:mm:ss).
            created_to (str): Filter by creation end date
                (YYYY-MM-DDTHH:mm:ss).
            sort_by (str): Field for sorting. Available: created-at, username.
                Default: created-at
            order (str): Sort order. Available: asc, desc. Default: asc
            limit (int): Max number of records
            offset (int): Start from

        Returns:
            UsersWithResourcesResponse
        """
        url = f"{self.base_url}/users-resources"
        params = {
            "search": search,
            "base-roles": ",".join(base_roles) if base_roles else None,
            "username": ",".join(usernames) if usernames else None,
            "empty-assignments": empty_assignments,
            "no-groups": no_groups,
            "created-from": created_from,
            "created-to": created_to,
            "sort-by": sort_by,
            "order": order,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return UsersWithResourcesResponse.from_dict(response.json())

    def retrieve_clients_with_resources(
        self,
        search: str = None,
        base_roles: List[str] = None,
        client_ids: List[str] = None,
        empty_assignments: bool = True,
        sort_by: str = "created-at",
        order: str = "asc",
        limit: int = None,
        offset: int = None,
        no_groups: bool = True,
        created_from: str = None,
        created_to: str = None,
    ) -> ClientsWithResourcesResponse:
        """
        Get a list of clients and the resources assigned to each client.
        Args:
            search (str): Search clients by client-id prefix.
            base_roles (List[str]): Filter by base roles (comma separated).
            client_ids (List[str]): Filter by client-id (comma separated).
            empty_assignments (bool): Filter by assignments.
            sort_by (str): Field for sorting. Available: created-at, client-id.
                Default: created-at
            order (str): Sort order. Available: asc, desc. Default: asc
            limit (int): Max number of results to return
            offset (int): Number of pages to skip.
            no_groups (bool): Filter clients by group membership.
            created_from (str): Filter by creation start date
                (YYYY-MM-DDTHH:mm:ss).
            created_to (str): Filter by creation end date
                (YYYY-MM-DDTHH:mm:ss).

        Returns:
            ClientsWithResourcesResponse
        """
        url = f"{self.base_url}/clients-resources"
        params = {
            "search": search,
            "base-roles": ",".join(base_roles) if base_roles else None,
            "client-id": ",".join(client_ids) if client_ids else None,
            "empty-assignments": empty_assignments,
            "sort-by": sort_by,
            "order": order,
            "limit": limit,
            "offset": offset,
            "no-groups": no_groups,
            "created-from": created_from,
            "created-to": created_to,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return ClientsWithResourcesResponse.from_dict(response.json())

    def retrieve_groups_with_resources(
        self,
        search: str = None,
        base_roles: List[str] = None,
        names: List[str] = None,
        empty_assignments: bool = True,
        no_members: bool = None,
        sort_by: str = "created-at",
        created_from: str = None,
        created_to: str = None,
        order: str = "asc",
        limit: int = None,
        offset: int = None,
    ) -> GroupsWithResourcesResponse:
        """
        Get a list of groups with resources assigned to each group.
        Args:
            search (str): Search groups by name prefix.
            base_roles (List[str]): Filter by base roles (comma separated).
            names (List[str]): Filter by name (comma separated).
            empty_assignments (bool): Filter by assignments.
            no_members (bool): Filter groups by user/client membership.
            sort_by (str): Field for sorting. Available: created-at, name.
                Default: created-at
            created_from (str): Filter by creation start date
                (YYYY-MM-DDTHH:mm:ss).
            created_to (str): Filter by creation end date
                (YYYY-MM-DDTHH:mm:ss).
            order (str): Sort order. Available: asc, desc. Default: asc
            limit (int): Max number of records
            offset (int): Start from

        Returns:
            GroupsWithResourcesResponse
        """
        url = f"{self.base_url}/groups-resources"
        params = {
            "search": search,
            "base-roles": ",".join(base_roles) if base_roles else None,
            "name": ",".join(names) if names else None,
            "empty-assignments": empty_assignments,
            "no-members": no_members,
            "sort-by": sort_by,
            "created-from": created_from,
            "created-to": created_to,
            "order": order,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return GroupsWithResourcesResponse.from_dict(response.json())

    def get_a_list_of_permissions_of_entity_for_resource(
        self,
        entity_id: str,
        entity_type: EntityType,
        resource_id: str = None,
        resource_type: ResourceType = None,
    ) -> EffectivePermissionsForResourceResponse:
        """
        Get a list of permissions of an entity (user, client, group) for
        a specific resource without specifying where they were assigned.
        Args:
            entity_id (str):
            entity_type (EntityType): Available values: user, client, group
            resource_id (str): Not required if resource-type is
                tenant/global.
            resource_type (ResourceType): Available values: project,
                application, tenantgroup, tenant, global

        Returns:
            EffectivePermissionsForResourceResponse
        """
        url = f"{self.base_url}/effective-permissions/{entity_id}"
        params = {
            "entity-type": entity_type,
            "resource-id": resource_id,
            "resource-type": resource_type,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return EffectivePermissionsForResourceResponse.from_dict(response.json())

    def get_a_list_of_applications_with_action_for_user_or_client(
        self,
        action: str,
        offset: int = 0,
        limit: int = 20,
        name: str = None,
        tags_keys: List[str] = None,
        tags_values: List[str] = None,
    ) -> ApplicationsCollection:
        """
        Get a list of applications for an entity (user, client) with
        a specific action (permission).
        Args:
            action (str):
            offset (int): Items to skip before collecting the result set.
                Default value: 0
            limit (int): Number of items to return. Default value: 20
            name (str): Application name, can be filtered by partial name.
            tags_keys (List[str]): Filter by tag keys (OR operation).
            tags_values (List[str]): Filter by tag values (OR operation).

        Returns:
            ApplicationsCollection
        """
        url = f"{self.base_url}/applications"
        params = {
            "action": action,
            "offset": offset,
            "limit": limit,
            "name": name,
            "tags-keys": tags_keys,
            "tags-values": tags_values,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return ApplicationsCollection.from_dict(response.json())

    def get_a_list_of_projects_with_action_for_user_or_client(
        self,
        action: str,
        offset: int = 0,
        limit: int = 20,
        name: str = None,
        tags_keys: List[str] = None,
        tags_values: List[str] = None,
    ) -> ProjectsCollection:
        """
        Get a list of projects for an entity (user, client) with a
        specific action (permission).
        Args:
            action (str):
            offset (int): Items to skip before collecting the result set.
                Default value: 0
            limit (int): Number of items to return. Default value: 20
            name (str): Project name, can be filtered by partial name.
            tags_keys (List[str]): Filter by tag keys (OR operation).
            tags_values (List[str]): Filter by tag values (OR operation).

        Returns:
            ProjectsCollection
        """
        url = f"{self.base_url}/projects"
        params = {
            "action": action,
            "offset": offset,
            "limit": limit,
            "name": name,
            "tags-keys": tags_keys,
            "tags-values": tags_values,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return ProjectsCollection.from_dict(response.json())

    def retrieve_user_or_client_groups(
        self,
        include_subgroups: bool = False,
        search: str = None,
        limit: int = None,
        offset: int = None,
    ) -> GroupsResponse:
        """
        Get a list of user/client groups to which the current user
        (as identified by JWT token) is assigned.
        Args:
            include_subgroups (bool): Set to true to include subgroups.
                Default value: false
            search (str): Search by group name
            limit (int): Max number of results to return
            offset (int): Number of pages to skip.

        Returns:
            GroupsResponse
        """
        url = f"{self.base_url}/my-groups"
        params = {
            "include-subgroups": include_subgroups,
            "search": search,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return GroupsResponse.from_dict(response.json())

    def retrieve_user_or_client_available_groups(
        self,
        project_id: str = None,
        search: str = None,
        limit: int = None,
        offset: int = None,
    ) -> GroupsResponse:
        """
        Get a list of groups available for user/client on
        project/global level.
        Args:
            project_id (str): The unique identifier of the project.
                If not provided, checks access on tenant level.
            search (str): Search by group name
            limit (int): Max number of results to return
            offset (int): Number of pages to skip.

        Returns:
            GroupsResponse
        """
        url = f"{self.base_url}/available-groups"
        params = {
            "project-id": project_id,
            "search": search,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return GroupsResponse.from_dict(response.json())

    def retrieve_groups(
        self,
        limit: int = None,
        offset: int = None,
        search: str = None,
        ids: List[str] = (),
    ) -> List[Group]:
        """
        Get info about user groups in the tenant account.
        Args:
            limit (int): Max number of results to return
            offset (int): Number of pages to skip.
            search (str): Search by group name
            ids (List[str]): Filter by group IDs (comma separated)

        Returns:
            List[Group]
        """
        url = f"{self.base_url}/groups"
        params = {
            "limit": limit,
            "offset": offset,
            "search": search,
            "ids": ",".join(ids) if ids else None,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return [Group.from_dict(g) for g in response.json()]

    def retrieve_users(
        self, limit: int = None, offset: int = None, search: str = None
    ) -> List[User]:
        """
        Get info about users in the tenant account.
        Args:
            limit (int): Max number of results to return
            offset (int): Number of pages to skip.
            search (str): Search by username, firstname, lastname or email

        Returns:
            List[User]
        """
        url = f"{self.base_url}/users"
        params = {"limit": limit, "offset": offset, "search": search}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return [User.from_dict(u) for u in response.json()]

    def retrieve_clients(self) -> List[Client]:
        """
        Get info about OAuth clients in the tenant account.

        Returns:
            List[Client]
        """
        url = f"{self.base_url}/clients"
        response = self.api_client.call_api(method="GET", url=url)
        return [Client.from_dict(c) for c in response.json()]

    def retrieve_users_from_internal_am_storage(self) -> dict:
        """
        Get info about users in the tenant account.
        This returns the same info as /users, but draws from the internal
        Access Management database for faster results.

        Returns:
            dict
        """
        url = f"{self.base_url}/internal/users"
        response = self.api_client.call_api(method="GET", url=url)
        item = response.json()
        return {
            "total": item.get("total"),
            "users": [InternalUser.from_dict(u) for u in (item.get("users") or [])],
        }

    def retrieve_groups_from_internal_am_storage(self) -> dict:
        """
        Get info about groups in the tenant account.
        This returns the same info as /groups, but draws from the internal
        Access Management database for faster results.

        Returns:
            dict
        """
        url = f"{self.base_url}/internal/groups"
        response = self.api_client.call_api(method="GET", url=url)
        item = response.json()
        return {
            "total": item.get("total"),
            "groups": [
                InternalGroup.from_dict(g) for g in (item.get("groups") or [])
            ],
        }

    def retrieve_clients_from_internal_am_storage(self) -> List[InternalClient]:
        """
        Get AM clients.

        Returns:
            List[InternalClient]
        """
        url = f"{self.base_url}/internal/clients"
        response = self.api_client.call_api(method="GET", url=url)
        return [InternalClient.from_dict(c) for c in response.json()]

    def retrieve_entity_base_roles(self, entity_id: str) -> BaseRolesResponse:
        """
        Get the base roles for a specific entity (user, group or client).
        'Base roles' are the set of permissions granted to the entity by
        default for assignments in which no roles were designated.

        Args:
            entity_id (str):

        Returns:
            BaseRolesResponse
        """
        url = f"{self.base_url}/base-roles/{entity_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return BaseRolesResponse.from_dict(response.json())

    def update_base_roles_for_an_entity(
        self, base_roles: BaseRolesRequest, entity_id: str
    ) -> bool:
        """
        Update the base roles for the specified entity.
        This will overwrite the existing base roles.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/base-roles/{entity_id}"
        response = self.api_client.call_api(
            method="PUT", url=url, json=asdict(base_roles)
        )
        return response.status_code == OK

    def assign_base_roles_to_an_entity(
        self, base_roles: BaseRolesRequest, entity_id: str
    ) -> bool:
        """
        Add base roles to the specified entity without overwriting existing
        roles. The body is an array of role IDs.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/base-roles/{entity_id}"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(base_roles)
        )
        return response.status_code == CREATED

    def delete_base_roles_for_an_entity(self, entity_id: str) -> bool:
        """
        Delete the base roles for a specific entity.
        Args:
            entity_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/base-roles/{entity_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def assign_base_roles_by_role_name(
        self, base_roles: BaseRolesRequest, entity_id: str
    ) -> bool:
        """
        Add base roles to the specified entity without overwriting existing
        roles. The body is an array of role names.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/base-roles/{entity_id}/by-name"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(base_roles)
        )
        return response.status_code == CREATED

    def unassign_base_roles_by_role_name(
        self, base_roles: BaseRolesRequest, entity_id: str
    ) -> bool:
        """
        Revoke base roles from an entity by specifying the role names.
        Args:
            base_roles (BaseRolesRequest):
            entity_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/base-roles/{entity_id}/by-name/unassign"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(base_roles)
        )
        return response.status_code == CREATED

    def retrieve_roles(self) -> List[RoleWithDetails]:
        """
        Get info about roles in the tenant account.

        Returns:
            List[RoleWithDetails]
        """
        url = f"{self.base_url}/roles"
        response = self.api_client.call_api(method="GET", url=url)
        return [RoleWithDetails.from_dict(r) for r in response.json()]

    def create_a_role(self, role_request: CreateRoleRequest) -> bool:
        """
        Creates a new role, specifying the series of permissions assigned
        to the new role. Roles can then be assigned to entities in the
        context of assignment creation.

        Returns:
            bool
        """
        url = f"{self.base_url}/roles"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(role_request)
        )
        return response.status_code == CREATED

    def retrieve_role(self, role_id: str) -> RoleWithDetails:
        """
        Get information about a specific role, specified by roleId.
        Args:
            role_id (str):

        Returns:
            RoleWithDetails
        """
        url = f"{self.base_url}/roles/{role_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return RoleWithDetails.from_dict(response.json())

    def update_a_role(self, role_request: CreateRoleRequest, role_id: str) -> bool:
        """
        Edit the configuration of an existing role. All parameters are
        overwritten by the new configuration. System roles cannot be
        updated.
        Args:
            role_request (CreateRoleRequest):
            role_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/roles/{role_id}"
        response = self.api_client.call_api(
            method="PUT", url=url, json=asdict(role_request)
        )
        return response.status_code == CREATED

    def delete_a_role(self, role_id: str) -> bool:
        """
        Deletes a role. System roles cannot be deleted.
        Args:
            role_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/roles/{role_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == OK

    def retrieve_permissions(self) -> List[Permission]:
        """
        Get info about all permissions that are available in the system.

        Returns:
            List[Permission]
        """
        url = f"{self.base_url}/permissions"
        response = self.api_client.call_api(method="GET", url=url)
        return [Permission.from_dict(p) for p in response.json()]


def create_an_assignment(assignment_input: AssignmentInput) -> bool:
    return AccessManagementAPI().create_an_assignment(
        assignment_input=assignment_input
    )


def delete_an_assignment(entity_id: str, resource_id: str) -> bool:
    return AccessManagementAPI().delete_an_assignment(
        entity_id=entity_id, resource_id=resource_id
    )


def retrieve_an_assignment(entity_id: str, resource_id: str) -> Assignment:
    return AccessManagementAPI().retrieve_an_assignment(
        entity_id=entity_id, resource_id=resource_id
    )


def update_assignment_roles(
    entity_roles: EntityRolesRequest, entity_id: str, resource_id: str
) -> bool:
    return AccessManagementAPI().update_assignment_roles(
        entity_roles=entity_roles, entity_id=entity_id, resource_id=resource_id
    )


def retrieve_resource_assignments(
    resource_ids: List[str],
) -> AssignmentsForResource:
    return AccessManagementAPI().retrieve_resource_assignments(
        resource_ids=resource_ids
    )


def create_multiple_assignments(
    multiple_assignment: MultipleAssignmentInput,
) -> bool:
    return AccessManagementAPI().create_multiple_assignments(
        multiple_assignment=multiple_assignment
    )


def add_roles_to_assignment(assignment_roles: AddAssignmentRoles) -> bool:
    return AccessManagementAPI().add_roles_to_assignment(
        assignment_roles=assignment_roles
    )


def retrieve_entities(
    resource_id: str,
    resource_type: ResourceType,
    entity_types: List[EntityType] = None,
) -> List[Assignment]:
    return AccessManagementAPI().retrieve_entities(
        resource_id=resource_id,
        resource_type=resource_type,
        entity_types=entity_types,
    )


def retrieve_extended_entities_for_resource(
    resource_id: str,
    resource_type: ResourceType,
    entity_types: List[EntityType] = None,
    sort_by: str = "entity_name",
    order: str = "asc",
    limit: int = 10,
    offset: int = 0,
    search: str = None,
) -> EntitiesForExtendedResponse:
    return AccessManagementAPI().retrieve_extended_entities_for_resource(
        resource_id=resource_id,
        resource_type=resource_type,
        entity_types=entity_types,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
        search=search,
    )


def retrieve_resources(
    entity_id: str, resource_types: List[ResourceType] = None
) -> List[Assignment]:
    return AccessManagementAPI().retrieve_resources(
        entity_id=entity_id, resource_types=resource_types
    )


def check_access(
    resource_id: str, resource_type: ResourceType, action: str
) -> bool:
    return AccessManagementAPI().check_access(
        resource_id=resource_id, resource_type=resource_type, action=action
    )


def check_access_to_requested_groups(
    group_ids: List[str], project_id: str = None
) -> bool:
    return AccessManagementAPI().check_access_to_requested_groups(
        group_ids=group_ids, project_id=project_id
    )


def retrieve_accessible_resources(
    resource_types: List[ResourceType], action: str
) -> ResourcesResponse:
    return AccessManagementAPI().retrieve_accessible_resources(
        resource_types=resource_types, action=action
    )


def retrieve_users_with_resources(
    search: str = None,
    base_roles: List[str] = None,
    usernames: List[str] = None,
    empty_assignments: bool = None,
    no_groups: bool = None,
    created_from: str = None,
    created_to: str = None,
    sort_by: str = "created-at",
    order: str = "asc",
    limit: int = None,
    offset: int = None,
) -> UsersWithResourcesResponse:
    return AccessManagementAPI().retrieve_users_with_resources(
        search=search,
        base_roles=base_roles,
        usernames=usernames,
        empty_assignments=empty_assignments,
        no_groups=no_groups,
        created_from=created_from,
        created_to=created_to,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


def retrieve_clients_with_resources(
    search: str = None,
    base_roles: str = None,
    client_ids: List[str] = None,
    empty_assignments: bool = None,
    sort_by: str = "created-at",
    order: str = "asc",
    limit: int = None,
    offset: int = None,
    no_groups: bool = None,
    created_from: str = None,
    created_to: str = None,
) -> ClientsWithResourcesResponse:
    return AccessManagementAPI().retrieve_clients_with_resources(
        search=search,
        base_roles=base_roles,
        client_ids=client_ids,
        empty_assignments=empty_assignments,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
        no_groups=no_groups,
        created_from=created_from,
        created_to=created_to,
    )


def retrieve_groups_with_resources(
    search: str = None,
    base_roles: str = None,
    names: List[str] = None,
    empty_assignments: bool = True,
    no_members: bool = True,
    sort_by: str = "created-at",
    created_from: str = None,
    created_to: str = None,
    order: str = "asc",
    limit: int = None,
    offset: int = None,
) -> GroupsWithResourcesResponse:
    return AccessManagementAPI().retrieve_groups_with_resources(
        search=search,
        base_roles=base_roles,
        names=names,
        empty_assignments=empty_assignments,
        no_members=no_members,
        sort_by=sort_by,
        created_from=created_from,
        created_to=created_to,
        order=order,
        limit=limit,
        offset=offset,
    )


def get_a_list_of_permissions_of_entity_for_resource(
    entity_id: str,
    entity_type: EntityType,
    resource_id: str = None,
    resource_type: ResourceType = None,
) -> EffectivePermissionsForResourceResponse:
    return AccessManagementAPI().get_a_list_of_permissions_of_entity_for_resource(
        entity_id=entity_id,
        entity_type=entity_type,
        resource_id=resource_id,
        resource_type=resource_type,
    )


def get_a_list_of_applications_with_action_for_user_or_client(
    action: str,
    offset: int = 0,
    limit: int = 20,
    name: str = None,
    tags_keys: List[str] = None,
    tags_values: List[str] = None,
) -> ApplicationsCollection:
    return AccessManagementAPI().get_a_list_of_applications_with_action_for_user_or_client(
        action=action,
        offset=offset,
        limit=limit,
        name=name,
        tags_keys=tags_keys,
        tags_values=tags_values,
    )


def get_a_list_of_projects_with_action_for_user_or_client(
    action: str,
    offset: int = 0,
    limit: int = 20,
    name: str = None,
    tags_keys: List[str] = None,
    tags_values: List[str] = None,
) -> ProjectsCollection:
    return AccessManagementAPI().get_a_list_of_projects_with_action_for_user_or_client(
        action=action,
        offset=offset,
        limit=limit,
        name=name,
        tags_keys=tags_keys,
        tags_values=tags_values,
    )


def retrieve_user_or_client_groups(
    include_subgroups: bool = False,
    search: str = None,
    limit: int = None,
    offset: int = None,
) -> GroupsResponse:
    return AccessManagementAPI().retrieve_user_or_client_groups(
        include_subgroups=include_subgroups,
        search=search,
        limit=limit,
        offset=offset,
    )


def retrieve_user_or_client_available_groups(
    project_id: str = None,
    search: str = None,
    limit: int = None,
    offset: int = None,
) -> GroupsResponse:
    return AccessManagementAPI().retrieve_user_or_client_available_groups(
        project_id=project_id,
        search=search,
        limit=limit,
        offset=offset,
    )


def retrieve_groups(
    limit: int = None, offset: int = None, search: str = None, ids: List[str] = None
) -> List[Group]:
    return AccessManagementAPI().retrieve_groups(
        limit=limit, offset=offset, search=search, ids=ids
    )


def retrieve_users(
    limit: int = None, offset: int = None, search: str = None
) -> List[User]:
    return AccessManagementAPI().retrieve_users(
        limit=limit, offset=offset, search=search
    )


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


def update_base_roles_for_an_entity(
    base_roles: BaseRolesRequest, entity_id: str
) -> bool:
    return AccessManagementAPI().update_base_roles_for_an_entity(
        base_roles=base_roles, entity_id=entity_id
    )


def assign_base_roles_to_an_entity(
    base_roles: BaseRolesRequest, entity_id: str
) -> bool:
    return AccessManagementAPI().assign_base_roles_to_an_entity(
        base_roles=base_roles, entity_id=entity_id
    )


def delete_base_roles_for_an_entity(entity_id: str) -> bool:
    return AccessManagementAPI().delete_base_roles_for_an_entity(entity_id)


def assign_base_roles_by_role_name(
    base_roles: BaseRolesRequest, entity_id: str
) -> bool:
    return AccessManagementAPI().assign_base_roles_by_role_name(
        base_roles=base_roles, entity_id=entity_id
    )


def unassign_base_roles_by_role_name(
    base_roles: BaseRolesRequest, entity_id: str
) -> bool:
    return AccessManagementAPI().unassign_base_roles_by_role_name(
        base_roles=base_roles, entity_id=entity_id
    )


def retrieve_roles() -> List[RoleWithDetails]:
    return AccessManagementAPI().retrieve_roles()


def create_a_role(role_request: CreateRoleRequest) -> bool:
    return AccessManagementAPI().create_a_role(role_request=role_request)


def retrieve_role(role_id: str) -> RoleWithDetails:
    return AccessManagementAPI().retrieve_role(role_id=role_id)


def update_a_role(role_request: CreateRoleRequest, role_id: str) -> bool:
    return AccessManagementAPI().update_a_role(
        role_request=role_request, role_id=role_id
    )


def delete_a_role(role_id: str) -> bool:
    return AccessManagementAPI().delete_a_role(role_id=role_id)


def retrieve_permissions() -> List[Permission]:
    return AccessManagementAPI().retrieve_permissions()
