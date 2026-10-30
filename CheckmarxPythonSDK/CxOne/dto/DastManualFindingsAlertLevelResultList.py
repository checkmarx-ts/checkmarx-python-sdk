from dataclasses import dataclass, field
from typing import List, Optional

from .DastManualFindingsAlertLevelResult import DastManualFindingsAlertLevelResult


@dataclass
class DastManualFindingsAlertLevelResultList:
    """Response from GET .../manual_findings/alert_level."""
    results: List[DastManualFindingsAlertLevelResult] = field(default_factory=list)
    total: Optional[int] = None
    pages_number: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastManualFindingsAlertLevelResultList":
        return cls(
            results=[
                DastManualFindingsAlertLevelResult.from_dict(r)
                for r in (item.get("results") or [])
            ],
            total=item.get("total"),
            pages_number=item.get("pages_number"),
        )
