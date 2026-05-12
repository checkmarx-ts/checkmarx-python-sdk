from dataclasses import dataclass
from typing import List


@dataclass
class EntityRolesRequest:
    """
    Specify the new roles that will be assigned to the entity
    for this assignment
    Attributes:
       newEntityRoles (List[str]): Specify the roles for this
       assignment. Note:This overwrites all existing roles.
    """

    newEntityRoles: List[str] = None
