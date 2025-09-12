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


def construct_client_with_resource(item):
    return ClientWithResource(
        id=item.get("id"),
        client_id=item.get("clientId"),
        iam_id=item.get("iamId"),
        created_at=item.get("createdAt"),
        group_ids=item.get("groupIds"),
        base_roles=item.get("baseRoles"),
        resources=[
            {
                "id": resource.get("id"),
                "type": resource.get("type"),
                "name": resource.get("name"),
                "roles": resource.get("roles")
            } for resource in item.get("resources")
        ]
    )
