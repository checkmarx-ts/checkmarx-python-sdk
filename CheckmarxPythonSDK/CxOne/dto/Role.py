from dataclasses import dataclass


@dataclass
class Role:
    id: str = None
    name: str = None
    description: str = None
    composite: bool = None
    client_role: bool = None
    container_id: str = None
    tenant_id: str = None
    system_role: bool = None
    created_at: str = None
    updated_at: str = None


def construct_role(item):
    return Role(
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        composite=item.get("composite"),
        client_role=item.get("clientRole"),
        container_id=item.get("containerId"),
        tenant_id=item.get("tenantId"),
        system_role=item.get("systemRole"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
    )
