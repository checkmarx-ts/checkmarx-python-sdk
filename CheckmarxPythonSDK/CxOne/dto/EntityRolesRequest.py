from dataclasses import dataclass
from typing import List


@dataclass
class EntityRolesRequest:
    """
    Specify the new roles that will be assigned to the entity for this assignment
    Attributes:
       new_entity_roles (List[str]): Specify the roles for this assignment. Note:This overwrites all existing roles.
    """
    new_entity_roles: List[str] = None

    def to_dict(self):
        return {
          "newEntityRoles": self.new_entity_roles
        }
