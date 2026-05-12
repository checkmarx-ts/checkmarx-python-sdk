from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class AssignmentsWithBaseRoles:
    entity_id: str = None
    entity_type: EntityType = None
    entity_name: str = None
    entity_roles: List[str] = None
    resource_id: str = None
    resource_type: ResourceType = None
    resource_name: str = None
    effective_permissions_count: int = None
    base_roles: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AssignmentsWithBaseRoles":
        return cls(
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
