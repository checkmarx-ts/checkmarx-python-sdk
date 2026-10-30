from dataclasses import dataclass, field
from typing import List, Optional

from .DastManualFindingInstanceResult import DastManualFindingInstanceResult


@dataclass
class DastManualFindingInstanceResultList:
    """Response from GET .../manual_findings."""
    results: List[DastManualFindingInstanceResult] = field(default_factory=list)
    total: Optional[int] = None
    pages_number: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastManualFindingInstanceResultList":
        return cls(
            results=[
                DastManualFindingInstanceResult.from_dict(r)
                for r in (item.get("results") or [])
            ],
            total=item.get("total"),
            pages_number=item.get("pages_number"),
        )
