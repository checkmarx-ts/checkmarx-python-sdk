from dataclasses import dataclass
from typing import List
from .GroupRepresentation import GroupRepresentation


@dataclass
class GroupsResponse:
    total: int = None
    groups: List[GroupRepresentation] = None

    @classmethod
    def from_dict(cls, item: dict) -> "GroupsResponse":
        return cls(
            total=item.get("total"),
            groups=[
                GroupRepresentation.from_dict(g) for g in (item.get("groups") or [])
            ],
        )
