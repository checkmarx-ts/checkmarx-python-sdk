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


def construct_user_with_resource(item):
    return UserWithResource(
        id=item.get("id"),
        user_name=item.get("username"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        created_at=item.get("createdAt"),
        base_roles=[
            {
                "id": role.get("id"),
                "name": role.get("name")
            } for role in item.get("baseRoles", [])
        ],
        groups=item.get("groups"),
        resources=[
            {
                "total": resource.get("total"),
                "applicationsCount": resource.get("applicationsCount"),
                "projectsCount": resource.get("projectsCount"),
                "tenantCount": resource.get("tenantCount")
            } for resource in item.get("resources", [])
        ]
    )
