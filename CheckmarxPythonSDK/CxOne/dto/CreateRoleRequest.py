from dataclasses import dataclass
from typing import List


@dataclass
class CreateRoleRequest:
    name: str = None
    description: str = None
    permissions: List[str] = None
