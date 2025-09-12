from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class AssignmentInput:
    """

    Attributes:
        entity_id (str): The unique identifier of the entity (user, group, client)
        entity_type (EntityType): Type of the entity. Enum: group, user, client
        resource_id (str): The unique identifier of the resource
        resource_type (ResourceType): Type of resource. Enum: application, project, tenant
        entity_roles (List[str]): Optional for AM phase 1. The roles assigned to the entity for this resource.
                                  Note: If no role is assigned, then the default "base" role is applied.
    """
    entity_id: str = None
    entity_type: EntityType = None
    resource_id: str = None
    resource_type: ResourceType = None
    entity_roles: List[str] = None

    def to_dict(self):
        return {
          "entityID": self.entity_id,
          "entityType": self.entity_type,
          "resourceID": self.resource_id,
          "resourceType": self.resource_type,
          "entityRoles": self.entity_roles,
        }
