from dataclasses import dataclass
from typing import Optional


@dataclass
class DastSequenceWithRecordingCount:
    """An entry in the response of GET /environments/{envId}/sequences."""
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    position: Optional[int] = None
    recordings_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequenceWithRecordingCount":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            created_at=item.get("createdAt"),
            created_by=item.get("createdBy"),
            position=item.get("position"),
            recordings_count=item.get("recordingsCount"),
        )
