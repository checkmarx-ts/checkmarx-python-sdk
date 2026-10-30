from dataclasses import dataclass
from typing import Optional


@dataclass
class DastTunnel:
    """An entry in `tunnels[]` on GET /tunnels."""
    id: Optional[str] = None
    tenant_id: Optional[str] = None
    tunnel_name: Optional[str] = None
    token: Optional[str] = None
    created_at: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastTunnel":
        return cls(
            id=item.get("id"),
            tenant_id=item.get("tenantId"),
            tunnel_name=item.get("tunnelName"),
            token=item.get("token"),
            created_at=item.get("createdAt"),
            name=item.get("name"),
        )
