from dataclasses import dataclass
from typing import List
from .EntityType import EntityType
from .ResourceType import ResourceType


@dataclass
class AssignmentInput:
    """

    Attributes:
        entityID (str): The unique identifier of the entity (user, group, client)
        entityType (EntityType): Type of the entity. Enum: group, user, client
        resourceID (str): The unique identifier of the resource
        resourceType (ResourceType): Type of resource. Enum: application, project, tenant
        entityRoles (List[str]): Optional for AM phase 1. The roles assigned to the entity for this resource.
                                  Note: If no role is assigned, then the default "base" role is applied.
    """

    entityID: str = None
    entityType: EntityType = None
    resourceID: str = None
    resourceType: ResourceType = None
    entityRoles: List[str] = None
