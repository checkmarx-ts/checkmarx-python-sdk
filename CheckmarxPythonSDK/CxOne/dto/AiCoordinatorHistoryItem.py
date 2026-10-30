from dataclasses import dataclass, field
from typing import List, Optional

from .AiCoordinatorHistoryCounts import AiCoordinatorHistoryCounts


@dataclass
class AiCoordinatorHistoryItem:
    """Single auto-action run in the History Tab (one list row)."""
    id: Optional[str] = None
    origin: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[str] = None
    project_name: Optional[str] = None
    scanners: List[str] = field(default_factory=list)
    counts: Optional[AiCoordinatorHistoryCounts] = None
    failure_reason: Optional[str] = None
    occurrence_count: int = 1

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorHistoryItem":
        counts = item.get("counts")
        return cls(
            id=item.get("id"),
            origin=item.get("origin"),
            status=item.get("status"),
            completed_at=item.get("completedAt"),
            project_name=item.get("projectName"),
            scanners=list(item.get("scanners") or []),
            counts=AiCoordinatorHistoryCounts.from_dict(counts) if counts else None,
            failure_reason=item.get("failureReason"),
            occurrence_count=item.get("occurrenceCount", 1),
        )
