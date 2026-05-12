from dataclasses import dataclass
from typing import List


@dataclass
class EffectivePermissionsForResourceResponse:
    entity_id: str = None
    entity_type: str = None
    resource_id: str = None
    resource_type: str = None
    permissions: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "EffectivePermissionsForResourceResponse":
        return cls(
            entity_id=item.get("entityId"),
            entity_type=item.get("entityType"),
            resource_id=item.get("resourceId"),
            resource_type=item.get("resourceType"),
            permissions=item.get("permissions"),
        )
