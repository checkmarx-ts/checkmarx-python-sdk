from dataclasses import dataclass, field
from typing import List, Optional

from .DastSequenceInfo import DastSequenceInfo


@dataclass
class DastRecordingWithSequences:
    """An entry in `recordings[]` on GET /environments/{envId}/recordings."""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    interactions_number: Optional[int] = None
    sequences: List[DastSequenceInfo] = field(default_factory=list)
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastRecordingWithSequences":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            created_by=item.get("createdBy"),
            created_at=item.get("createdAt"),
            interactions_number=item.get("interactionsNumber"),
            sequences=[
                DastSequenceInfo.from_dict(s) for s in (item.get("sequences") or [])
            ],
            type=item.get("type"),
        )
