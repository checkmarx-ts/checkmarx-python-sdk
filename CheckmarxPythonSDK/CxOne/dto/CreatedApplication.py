from dataclasses import dataclass
from typing import List
from .Rule import Rule


@dataclass
class CreatedApplication:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        criticality (int):
        rules (`list` of `Rule`):
        tags (dict):
        created_at (str):
        updated_at (str):
    """

    id: str
    name: str
    description: str
    criticality: int
    rules: List[Rule]
    tags: dict
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, item: dict) -> "CreatedApplication":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            criticality=item.get("criticality"),
            rules=[Rule.from_dict(r) for r in (item.get("rules") or [])],
            tags=item.get("tags"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
        )
