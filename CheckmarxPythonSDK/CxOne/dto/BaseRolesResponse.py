from dataclasses import dataclass
from typing import List


@dataclass
class BaseRolesResponse:
    tenant_id: str = None
    entity_id: str = None
    base_roles: List[str] = None


def construct_base_roles_response(item):
    return BaseRolesResponse(
        tenant_id=item.get("tenantID"),
        entity_id=item.get("entityID"),
        base_roles=item.get("baseRoles"),
    )
