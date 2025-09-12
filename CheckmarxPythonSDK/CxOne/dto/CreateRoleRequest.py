from dataclasses import dataclass
from typing import List


@dataclass
class CreateRoleRequest:
    name: str = None
    description: str = None
    permissions: List[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
        }
