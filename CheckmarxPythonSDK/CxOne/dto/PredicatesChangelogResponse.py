from dataclasses import dataclass, field
from typing import List

from .PredicateChangelogGroup import PredicateChangelogGroup


@dataclass
class PredicatesChangelogResponse:
    """Response from GET /api/sast-results-predicates/changelog."""
    results: List[PredicateChangelogGroup] = field(default_factory=list)
    total_similarity_ids: str = None  # e.g. "presenting 6 of 11"

    @classmethod
    def from_dict(cls, item: dict) -> "PredicatesChangelogResponse":
        if not item:
            return None
        return cls(
            results=[
                PredicateChangelogGroup.from_dict(r)
                for r in (item.get("results") or [])
            ],
            total_similarity_ids=item.get("totalSimilarityIds"),
        )
