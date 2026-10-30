from dataclasses import dataclass
from typing import Optional


@dataclass
class DastRecording:
    """Response from POST /recordings (one per item) and
    PUT /recordings/{recordingId}."""
    id: Optional[str] = None
    tenant_id: Optional[str] = None
    environment_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    interactions_number: Optional[int] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastRecording":
        return cls(
            id=item.get("id"),
            tenant_id=item.get("tenantId"),
            environment_id=item.get("environmentId"),
            name=item.get("name"),
            description=item.get("description"),
            interactions_number=item.get("interactionsNumber"),
            created_at=item.get("createdAt"),
            created_by=item.get("createdBy"),
            type=item.get("type"),
        )
