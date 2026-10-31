from dataclasses import dataclass


@dataclass
class PredicatesStatus:
    """Response from POST /api/sast-results-predicates/predicates-status."""
    is_update_predicates_running: bool = None
    grouping_mode: str = None  # "Similarity ID" or "Attack Vector ID"

    @classmethod
    def from_dict(cls, item: dict) -> "PredicatesStatus":
        if not item:
            return None
        return cls(
            is_update_predicates_running=item.get("isUpdatePredicatesRunning"),
            grouping_mode=item.get("groupingMode"),
        )
