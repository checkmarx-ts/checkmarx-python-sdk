from dataclasses import dataclass
from typing import List


@dataclass
class RoleWithDetails:
    id: str = None
    tenant_id: str = None
    name: str = None
    description: str = None
    system_role: bool = None
    created_at: str = None
    updated_at: str = None
    permissions: List[str] = None
    custom_permissions: List[str] = None
    attributes: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RoleWithDetails":
        return cls(
            id=item.get("id"),
            tenant_id=item.get("tenantID"),
            name=item.get("name"),
            description=item.get("description"),
            system_role=item.get("systemRole"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
            permissions=item.get("permissions"),
            custom_permissions=item.get("customPermissions"),
            attributes=[
                {"name": a.get("name"), "value": a.get("value")}
                for a in (item.get("attributes") or [])
            ],
        )
