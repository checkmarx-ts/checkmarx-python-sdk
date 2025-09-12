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


def construct_group_with_resource(item):
    return GroupWithResource(
        id=item.get("id"),
        name=item.get("name"),
        path=item.get("path"),
        created_at=item.get("createdAt"),
        base_roles=[
            {
                "id": role.get("id"),
                "name": role.get("name")
            } for role in item.get("baseRoles")
        ],
        members={
            "totalCount": item.get("members").get("totalCount"),
            "usersCount": item.get("members").get("usersCount"),
            "clientsCount": item.get("members").get("clientsCount")
        },
        resources=[
            {
                "id": resource.get("id"),
                "type": resource.get("type"),
                "name": resource.get("name"),
                "roles": resource.get("roles")
            } for resource in item.get("resources")
        ]
    )
