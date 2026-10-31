from dataclasses import dataclass
from typing import Optional


@dataclass
class SimilarResultGroup:
    """An entry in SimilarResultsResponse.similar_results (POST
    /api/sast-results/similar-results) -- tells you how many results
    are similar to one given result hash, and whether they're
    currently in a consistent state.
    """
    id: Optional[str] = None  # the similarity/attack-vector id this result belongs to
    result_hash: Optional[str] = None
    similar_results_count: Optional[int] = None
    is_state_inconsistent: Optional[bool] = None
    is_severity_inconsistent: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SimilarResultGroup":
        if not item:
            return None
        return cls(
            id=item.get("id"),
            result_hash=item.get("resultHash"),
            similar_results_count=item.get("similarResultsCount"),
            is_state_inconsistent=item.get("isStateInconsistent"),
            is_severity_inconsistent=item.get("isSeverityInconsistent"),
        )
