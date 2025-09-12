from dataclasses import dataclass
from typing import List


@dataclass
class BaseRolesRequest:
    base_roles: List[str] = None

    def to_dict(self):
        return {
          "baseRoles": self.base_roles
        }
