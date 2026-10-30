from dataclasses import dataclass
from typing import Optional


@dataclass
class DastTunnelResponse:
    """Response from GET /tunnel/{tunnelId} and GET /tunnelByName/{name}."""
    id: Optional[str] = None
    tenant_id: Optional[str] = None
    tunnel_name: Optional[str] = None
    name: Optional[str] = None
    token: Optional[str] = None
    state: Optional[str] = None
    zrok_host: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastTunnelResponse":
        return cls(
            id=item.get("id"),
            tenant_id=item.get("tenantId"),
            tunnel_name=item.get("tunnelName"),
            name=item.get("name"),
            token=item.get("token"),
            state=item.get("state"),
            zrok_host=item.get("zrokHost"),
        )
