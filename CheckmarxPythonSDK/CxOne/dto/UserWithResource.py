from dataclasses import dataclass
from typing import List


@dataclass
class UserWithResource:
    id: str = None
    user_name: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    created_at: str = None
    base_roles: List[dict] = None
    groups: List[str] = None
    resources: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "UserWithResource":
        return cls(
            id=item.get("id"),
            user_name=item.get("username"),
            first_name=item.get("firstName"),
            last_name=item.get("lastName"),
            email=item.get("email"),
            created_at=item.get("createdAt"),
            base_roles=[
                {"id": r.get("id"), "name": r.get("name")}
                for r in (item.get("baseRoles") or [])
            ],
            groups=item.get("groups"),
            resources=[
                {
                    "total": r.get("total"),
                    "applicationsCount": r.get("applicationsCount"),
                    "projectsCount": r.get("projectsCount"),
                    "tenantCount": r.get("tenantCount"),
                }
                for r in (item.get("resources") or [])
            ],
        )
