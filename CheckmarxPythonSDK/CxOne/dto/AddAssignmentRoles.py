from dataclasses import dataclass
from typing import List


@dataclass
class AddAssignmentRoles:
    entityId: str = None
    resourceId: str = None
    entityRoles: List[str] = None
