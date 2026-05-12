from dataclasses import dataclass
from typing import List


@dataclass
class ClientWithResource:
    id: str = None
    client_id: str = None
    iam_id: str = None
    created_at: str = None
    group_ids: List[str] = None
    base_roles: List[str] = None
    resources: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientWithResource":
        return cls(
            id=item.get("id"),
            client_id=item.get("clientId"),
            iam_id=item.get("iamId"),
            created_at=item.get("createdAt"),
            group_ids=item.get("groupIds"),
            base_roles=item.get("baseRoles"),
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
