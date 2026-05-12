from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class MultipleAssignmentInput:
    """
    Attributes:
        entityType (EntityType): type of entity.
            Enum:[ group, user, client ]
        resourceType (ResourceType): type of resource.
            Enum:  [ application, project, tenant ]
        entityRoles (List[str]): The roles assigned for these
            assignments. Note: If no role is assigned, then the
            default "base" role is applied for each entity.
        entities (List[str]):
        resources (List[str]):
    """

    entityType: EntityType = None
    resourceType: ResourceType = None
    entityRoles: List[str] = None
    entities: List[str] = None
    resources: List[str] = None
