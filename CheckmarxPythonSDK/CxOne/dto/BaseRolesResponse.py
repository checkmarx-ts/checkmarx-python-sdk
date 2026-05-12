from dataclasses import dataclass
from typing import List


@dataclass
class BaseRolesResponse:
    tenant_id: str = None
    entity_id: str = None
    base_roles: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "BaseRolesResponse":
        return cls(
            tenant_id=item.get("tenantID"),
            entity_id=item.get("entityID"),
            base_roles=item.get("baseRoles"),
        )
