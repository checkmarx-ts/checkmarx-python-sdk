from dataclasses import dataclass
from typing import Optional


@dataclass
class Team:
    id: Optional[int] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    parent_id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Team":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            full_name=item.get("fullName"),
            parent_id=item.get("parentId"),
        )
