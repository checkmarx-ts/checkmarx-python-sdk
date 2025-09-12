from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class Assignment:
    """

    Attributes:
        tenant_id (str): ID of the tenant
        entity_id (str): The unique identifier of the entity
        entity_type (EntityType): Type of the entity Enum: [ group, user, client ]
        entity_name (str): Human-readable name of the entity
        entity_roles (List[str]): The roles assigned to the entity for this resource. Note: If no role is assigned, then
                                  the default "base" role is applied
        resource_id (str): The unique identifier of the resource
        resource_type (ResourceType): type of resource  Enum:[ application, project, tenant ]
        resource_name (str): Human-readable name of the resource
    """
    tenant_id: str = None
    entity_id: str = None
    entity_type: EntityType = None
    entity_name: str = None
    entity_roles: List[str] = None
    resource_id: str = None
    resource_type: ResourceType = None
    resource_name: str = None


def construct_assignment(item):
    return Assignment(
        tenant_id=item.get("tenantID"),
        entity_id=item.get("entityID"),
        entity_type=EntityType(item.get("entityType")),
        entity_name=item.get("entityName"),
        entity_roles=item.get("entityRoles"),
        resource_id=item.get("resourceID"),
        resource_type=ResourceType(item.get("resourceType")),
        resource_name=item.get("resourceName"),
    )
