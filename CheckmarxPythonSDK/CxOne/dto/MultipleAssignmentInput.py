from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class MultipleAssignmentInput:
    """
    Attributes:
        entity_type (EntityType): type of entity. Enum:[ group, user, client ]
        resource_type (ResourceType): type of resource. Enum:  [ application, project, tenant ]
        entity_roles (List[str]): The roles assigned for these assignments. Note: If no role is assigned, then the
                                  default "base" role is applied for each entity.
        entities (List[str]):
        resources (List[str]):
    """

    entity_type: EntityType = None
    resource_type: ResourceType = None
    entity_roles: List[str] = None
    entities: List[str] = None
    resources: List[str] = None

    def to_dict(self):
        return {
          "entityType": EntityType(self.entity_type),
          "resourceType": ResourceType(self.resource_type),
          "entityRoles": self.entity_roles,
          "entities": self.entities,
          "resources": self.resources
        }
