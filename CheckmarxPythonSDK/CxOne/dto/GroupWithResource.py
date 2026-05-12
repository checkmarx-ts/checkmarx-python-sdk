from dataclasses import dataclass
from typing import List


@dataclass
class GroupWithResource:
    id: str = None
    name: str = None
    path: str = None
    created_at: str = None
    base_roles: List[dict] = None
    members: dict = None
    resources: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "GroupWithResource":
        members = item.get("members") or {}
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            path=item.get("path"),
            created_at=item.get("createdAt"),
            base_roles=[
                {"id": r.get("id"), "name": r.get("name")}
                for r in (item.get("baseRoles") or [])
            ],
            members={
                "totalCount": members.get("totalCount"),
                "usersCount": members.get("usersCount"),
                "clientsCount": members.get("clientsCount"),
            },
            resources=[
                {
                    "id": r.get("id"),
                    "type": r.get("type"),
                    "name": r.get("name"),
                    "roles": r.get("roles"),
                }
                for r in (item.get("resources") or [])
            ],
        )
