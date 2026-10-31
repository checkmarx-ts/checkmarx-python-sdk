from dataclasses import dataclass, field
from typing import List, Optional

from .SimilarResultGroup import SimilarResultGroup


@dataclass
class SimilarResultsResponse:
    """Response from POST /api/sast-results/similar-results.

    Note: totalCounts and groupingMode are top-level fields (verified
    live), not nested inside each similarResults[] entry as the
    public doc's flattened schema view implies.
    """
    similar_results: List[SimilarResultGroup] = field(default_factory=list)
    total_counts: Optional[int] = None
    grouping_mode: Optional[str] = None  # "Similarity ID" or "Attack Vector ID"

    @classmethod
    def from_dict(cls, item: dict) -> "SimilarResultsResponse":
        if not item:
            return None
        return cls(
            similar_results=[
                SimilarResultGroup.from_dict(r)
                for r in (item.get("similarResults") or [])
            ],
            total_counts=item.get("totalCounts"),
            grouping_mode=item.get("groupingMode"),
        )
