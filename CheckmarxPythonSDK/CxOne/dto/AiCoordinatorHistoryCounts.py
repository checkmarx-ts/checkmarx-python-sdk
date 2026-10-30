from dataclasses import dataclass
from typing import Optional


@dataclass
class AiCoordinatorHistoryCounts:
    """Per-run finding counts, nested on AiCoordinatorHistoryItem."""
    processed: Optional[int] = None
    succeeded: Optional[int] = None
    failed: Optional[int] = None
    skipped: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorHistoryCounts":
        return cls(
            processed=item.get("processed"),
            succeeded=item.get("succeeded"),
            failed=item.get("failed"),
            skipped=item.get("skipped"),
        )
