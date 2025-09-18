from dataclasses import dataclass
from typing import List


@dataclass
class AddAssignmentRoles:
    entity_id: str = None
    resource_id: str = None
    entity_roles: List[str] = None

    def to_dict(self):
        return {
          "entityId": self.entity_id,
          "resourceId": self.resource_id,
          "entityRoles": self.entity_roles
        }


def construct_add_assignment_role(item):
    return AddAssignmentRoles(
        entity_id=item.get("entityId"),
        resource_id=item.get("resourceId"),
        entity_roles=item.get("entityRoles"),
    )
