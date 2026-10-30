from dataclasses import dataclass
from typing import Optional


@dataclass
class DastRecordingWithPosition:
    """An entry in the response of
    GET /environments/{envId}/sequences/{sequenceId}/recordings."""
    id: Optional[str] = None
    name: Optional[str] = None
    position: Optional[int] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastRecordingWithPosition":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            position=item.get("position"),
            created_at=item.get("createdAt"),
        )
