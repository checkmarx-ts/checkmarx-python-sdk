from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class AssignmentsWithBaseRoles:
    entity_id: str = None  # The unique identifier of the entity
    entity_type: EntityType = None  # Type of the entity [ group, user, client ]
    entity_name: str = None  # Human-readable name of the entity
    entity_roles: List[str] = None  # The roles assigned to the entity for this resource. Note: If no role is assigned,
    # then the default "base" role is applied.
    resource_id: str = None  # The unique identifier of the resource
    resource_type: ResourceType = None  # The type of resource [ application, project, tenant ]
    resource_name: str = None  # Human-readable name of the resource
    effective_permissions_count: int = None  # The number of effective permissions for the entity on the resource
    base_roles: List[str] = None  # Role names of only directly assigned base roles


def construct_assignments_with_base_roles(item):
    return AssignmentsWithBaseRoles(
        entity_id=item.get("entityID"),
        entity_type=EntityType(item.get("entityType")),
        entity_name=item.get("entityName"),
        entity_roles=item.get("entityRoles"),
        resource_id=item.get("resourceID"),
        resource_type=ResourceType(item.get("resourceType")),
        resource_name=item.get("resourceName"),
        effective_permissions_count=item.get("effectivePermissionsCount"),
        base_roles=item.get("baseRoles"),
    )
