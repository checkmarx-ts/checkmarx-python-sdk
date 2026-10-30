from dataclasses import dataclass
from typing import Optional


@dataclass
class DastCreateTunnelResponse:
    """Response from POST /tunnel."""
    id: Optional[str] = None
    name: Optional[str] = None
    tunnel_name: Optional[str] = None
    token: Optional[str] = None
    associated: Optional[bool] = None
    associated_err: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCreateTunnelResponse":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            tunnel_name=item.get("tunnelName"),
            token=item.get("token"),
            associated=item.get("associated"),
            associated_err=item.get("associatedErr"),
        )
