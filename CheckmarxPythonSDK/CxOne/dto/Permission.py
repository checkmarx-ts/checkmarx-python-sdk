from dataclasses import dataclass
from typing import List


@dataclass
class Permission:
    id: str = None
    name: str = None
    description: str = None
    child_ids: List[str] = None
    parent_ids: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Permission":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            child_ids=item.get("childIds"),
            parent_ids=item.get("parentIds"),
        )
