from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Role:
    id: Optional[int] = None
    is_system_role: Optional[bool] = None
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Role":
        return cls(
            id=item.get("id"),
            is_system_role=item.get("isSystemRole"),
            name=item.get("name"),
            description=item.get("description"),
            permission_ids=item.get("permissionIds"),
        )
