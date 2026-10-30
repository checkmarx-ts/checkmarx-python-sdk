from dataclasses import dataclass, field
from typing import List, Optional

from .DastAlertLevelResult import DastAlertLevelResult


@dataclass
class DastAlertLevelResultList:
    """Response from GET/POST .../alert_level."""
    results: List[DastAlertLevelResult] = field(default_factory=list)
    total: Optional[int] = None
    pages_number: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertLevelResultList":
        return cls(
            results=[
                DastAlertLevelResult.from_dict(r) for r in (item.get("results") or [])
            ],
            total=item.get("total"),
            pages_number=item.get("pages_number"),
        )
