from dataclasses import dataclass
from typing import List
from .UserWithResource import UserWithResource


@dataclass
class UsersWithResourcesResponse:
    total_count: None = None
    filtered_count: None = None
    users: List[UserWithResource] = None

    @classmethod
    def from_dict(cls, item: dict) -> "UsersWithResourcesResponse":
        return cls(
            total_count=item.get("totalCount"),
            filtered_count=item.get("filteredCount"),
            users=[UserWithResource.from_dict(u) for u in (item.get("users") or [])],
        )
