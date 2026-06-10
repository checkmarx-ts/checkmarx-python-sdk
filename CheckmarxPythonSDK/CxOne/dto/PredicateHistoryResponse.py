from dataclasses import dataclass, field
from typing import List

from .PredicateHistory import PredicateHistory


@dataclass
class PredicateHistoryResponse:
    """Full response from GET /sast-results-predicates/{similarityId}
    and GET /sast-results-predicates/{similarityId}/latest."""

    predicate_history_per_project: List[PredicateHistory] = field(default_factory=list)
    total_count: int = 0

    @classmethod
    def from_dict(cls, item: dict) -> "PredicateHistoryResponse":
        if not item:
            return None
        return cls(
            predicate_history_per_project=[
                PredicateHistory.from_dict(p)
                for p in (item.get("predicateHistoryPerProject") or [])
            ],
            total_count=item.get("totalCount", 0),
        )
