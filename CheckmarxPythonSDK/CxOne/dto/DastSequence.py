from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastSequence:
    """Response from POST /sequences, PUT /sequences/{sequenceId}, and
    POST /environments/{envId}/sequences/{sequenceId}/duplicate."""
    id: Optional[str] = None
    environment_id: Optional[str] = None
    name: Optional[str] = None
    position: Optional[int] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    recording_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequence":
        return cls(
            id=item.get("id"),
            environment_id=item.get("environmentId"),
            name=item.get("name"),
            position=item.get("position"),
            created_at=item.get("createdAt"),
            created_by=item.get("createdBy"),
            recording_ids=list(item.get("recordingIds") or []),
        )
