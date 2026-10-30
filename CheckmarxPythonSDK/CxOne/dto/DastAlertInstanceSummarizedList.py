from dataclasses import dataclass, field
from typing import List, Optional

from .DastAlertInstance import DastAlertInstance


@dataclass
class DastAlertInstanceSummarizedList:
    """Response from GET .../alert/{alert_id}/instances."""
    instances: List[DastAlertInstance] = field(default_factory=list)
    total: Optional[int] = None
    pages_number: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertInstanceSummarizedList":
        return cls(
            instances=[
                DastAlertInstance.from_dict(i) for i in (item.get("instances") or [])
            ],
            total=item.get("total"),
            pages_number=item.get("pages_number"),
        )
