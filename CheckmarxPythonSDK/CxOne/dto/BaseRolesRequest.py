from dataclasses import dataclass
from typing import List


@dataclass
class BaseRolesRequest:
    baseRoles: List[str] = None
