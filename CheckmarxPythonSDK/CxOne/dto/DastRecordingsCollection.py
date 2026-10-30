from dataclasses import dataclass, field
from typing import List, Optional

from .DastRecordingWithSequences import DastRecordingWithSequences


@dataclass
class DastRecordingsCollection:
    """Response from GET /environments/{envId}/recordings."""
    recordings: List[DastRecordingWithSequences] = field(default_factory=list)
    total_items: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastRecordingsCollection":
        return cls(
            recordings=[
                DastRecordingWithSequences.from_dict(r)
                for r in (item.get("recordings") or [])
            ],
            total_items=item.get("totalItems"),
        )
