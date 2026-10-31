from dataclasses import dataclass, field
from typing import List

from .PredicateWithCommentsJSON import PredicateWithCommentsJSON


@dataclass
class LatestPredicateResponse:
    """Full response from GET /sast-results-predicates/{similarityId}/latest.

    Not the same shape as PredicateHistoryResponse (the plain
    /{similarityId} endpoint): the top-level key here is
    latestPredicatePerProject (flat predicate fields per project), not
    predicateHistoryPerProject (each project wrapping a nested
    predicates[] list).
    """
    latest_predicate_per_project: List[PredicateWithCommentsJSON] = field(
        default_factory=list
    )
    total_count: int = 0

    @classmethod
    def from_dict(cls, item: dict) -> "LatestPredicateResponse":
        if not item:
            return None
        return cls(
            latest_predicate_per_project=[
                PredicateWithCommentsJSON.from_dict(p)
                for p in (item.get("latestPredicatePerProject") or [])
            ],
            total_count=item.get("totalCount", 0),
        )
