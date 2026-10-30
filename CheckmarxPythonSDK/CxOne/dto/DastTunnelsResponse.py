from dataclasses import dataclass, field
from typing import List, Optional

from .DastTunnel import DastTunnel


@dataclass
class DastTunnelsResponse:
    """Response from GET /tunnels."""
    tunnels: List[DastTunnel] = field(default_factory=list)
    zrok_host: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastTunnelsResponse":
        return cls(
            tunnels=[DastTunnel.from_dict(t) for t in (item.get("tunnels") or [])],
            zrok_host=item.get("zrokHost"),
        )
