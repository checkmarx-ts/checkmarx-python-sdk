from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .CloudConnectionStatus import CloudConnectionStatus


@dataclass
class CloudConnectionItem:
    """An entry in CloudConnectionsResponse.cloud_connections (one row
    in GET /api/cloud-connect/connections).

    status/status_message/refresh_date are deprecated server-side in
    favor of `statuses` (one entry per consumer of the connection), but
    kept here since the server still returns them.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    vendor: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    status: Optional[str] = None
    status_message: Optional[str] = None
    refresh_date: Optional[str] = None
    updated_at: Optional[str] = None
    statuses: List[CloudConnectionStatus] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CloudConnectionItem":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            vendor=item.get("vendor"),
            tags=dict(item.get("tags") or {}),
            status=item.get("status"),
            status_message=item.get("statusMessage"),
            refresh_date=item.get("refreshDate"),
            updated_at=item.get("updatedAt"),
            statuses=[
                CloudConnectionStatus.from_dict(s)
                for s in (item.get("statuses") or [])
            ],
        )
