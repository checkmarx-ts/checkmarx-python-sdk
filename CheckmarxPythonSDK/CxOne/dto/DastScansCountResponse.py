from dataclasses import dataclass, field
from typing import List, Optional

from .DastScansCountBySource import DastScansCountBySource


@dataclass
class DastScansCountResponse:
    """Response from GET /overview/scansCount/{envId}."""
    total: Optional[int] = None
    count_by_source: List[DastScansCountBySource] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastScansCountResponse":
        return cls(
            total=item.get("total"),
            count_by_source=[
                DastScansCountBySource.from_dict(s)
                for s in (item.get("countBySource") or [])
            ],
        )
