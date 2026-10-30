from dataclasses import dataclass, field
from typing import List

from .DastScansOverTime import DastScansOverTime


@dataclass
class DastScansOverTimeResponse:
    """Response from GET /environment/{envId}/scans-over-time."""
    scans_over_time: List[DastScansOverTime] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastScansOverTimeResponse":
        return cls(
            scans_over_time=[
                DastScansOverTime.from_dict(s) for s in (item.get("scansOverTime") or [])
            ],
        )
