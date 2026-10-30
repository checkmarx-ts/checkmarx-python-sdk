from dataclasses import dataclass, field
from typing import List, Optional

from .DastStateCount import DastStateCount


@dataclass
class DastResultsStatesSummary:
    """Response from GET /states_summary/{app_id}."""
    state_counts: List[DastStateCount] = field(default_factory=list)
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResultsStatesSummary":
        return cls(
            state_counts=[
                DastStateCount.from_dict(s) for s in (item.get("state_counts") or [])
            ],
            total=item.get("total"),
        )
