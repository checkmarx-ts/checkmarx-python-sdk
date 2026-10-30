from dataclasses import dataclass, field
from typing import List, Optional

from .CloudConnectionItem import CloudConnectionItem


@dataclass
class CloudConnectionsResponse:
    """Response from GET /api/cloud-connect/connections."""
    total_count: Optional[int] = None
    total_filtered_count: Optional[int] = None
    cloud_connections: List[CloudConnectionItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CloudConnectionsResponse":
        return cls(
            total_count=item.get("totalCount"),
            total_filtered_count=item.get("totalFilteredCount"),
            cloud_connections=[
                CloudConnectionItem.from_dict(c)
                for c in (item.get("cloudConnections") or [])
            ],
        )
