from dataclasses import dataclass


@dataclass
class Role:
    id: str = None
    tenant_id: str = None
    name: str = None
    description: str = None
    system_role: bool = None
    created_at: str = None
    updated_at: str = None


def construct_role(item):
    return Role(
        id=item.get("id"),
        tenant_id=item.get("tenantId"),
        name=item.get("name"),
        description=item.get("description"),
        system_role=item.get("systemRole"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
    )