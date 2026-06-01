from dataclasses import dataclass
from typing import List
from .DastResult import DastResult


@dataclass
class DastResultsCollection:
    """Top-level response of GET /api/dast/mfe-results/results/{scan_id}."""
    results: List[DastResult] = None
    total: int = None
    pages_number: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResultsCollection":
        return cls(
            results=[DastResult.from_dict(r) for r in (item.get("results") or [])],
            total=item.get("total"),
            pages_number=item.get("pages_number"),
        )
