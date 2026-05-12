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
        entity_roles (List[str]): The roles assigned to the entity for this resource.
        resource_id (str): The unique identifier of the resource
        resource_type (ResourceType): type of resource Enum: [ application, project, tenant ]
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
    created_at: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "Assignment":
        return cls(
            tenant_id=item.get("tenantID"),
            entity_id=item.get("entityID"),
            entity_type=EntityType(item.get("entityType")),
            entity_name=item.get("entityName"),
            entity_roles=item.get("entityRoles"),
            resource_id=item.get("resourceID"),
            resource_type=ResourceType(item.get("resourceType")),
            resource_name=item.get("resourceName"),
            created_at=item.get("createdAt"),
        )
