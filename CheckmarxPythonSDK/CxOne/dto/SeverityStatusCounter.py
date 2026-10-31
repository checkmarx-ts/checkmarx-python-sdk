from dataclasses import dataclass, field
from typing import List, Optional

from .CompareStatusCount import CompareStatusCount


@dataclass
class SeverityStatusCounter:
    """An entry in SastComparisonStatus.severity_status_counters --
    the status breakdown (NEW/RECURRENT/FIXED) for one severity level.
    """
    severity: Optional[str] = None
    results: List[CompareStatusCount] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "SeverityStatusCounter":
        if not item:
            return None
        return cls(
            severity=item.get("severity"),
            results=[
                CompareStatusCount.from_dict(r)
                for r in (item.get("results") or [])
            ],
        )
