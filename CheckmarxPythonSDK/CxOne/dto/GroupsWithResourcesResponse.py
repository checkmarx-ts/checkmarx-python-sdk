from dataclasses import dataclass
from typing import List
from .GroupWithResource import GroupWithResource


@dataclass
class GroupsWithResourcesResponse:
    total_count: int = None
    filtered_count: int = None
    groups: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "GroupsWithResourcesResponse":
        return cls(
            total_count=item.get("totalCount"),
            filtered_count=item.get("filteredCount"),
            groups=[GroupWithResource.from_dict(g) for g in (item.get("groups") or [])],
        )
