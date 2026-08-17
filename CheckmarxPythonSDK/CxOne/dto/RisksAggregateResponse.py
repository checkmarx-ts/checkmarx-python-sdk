from dataclasses import dataclass, field
from typing import List

from .RiskCounter import RiskCounter


@dataclass
class RisksAggregateResponse:
    """Response from GET /api/risks/aggregate.

    Attributes:
        risksCounters (List[RiskCounter]): Aggregated risk counters grouped
            by the requested dimensions (severity, engine, or both).
    """

    risksCounters: List[RiskCounter] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "RisksAggregateResponse":
        return cls(
            risksCounters=[
                RiskCounter.from_dict(c)
                for c in (item.get("risksCounters") or [])
            ]
        )
