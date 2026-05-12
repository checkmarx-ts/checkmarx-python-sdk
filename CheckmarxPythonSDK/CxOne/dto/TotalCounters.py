from dataclasses import dataclass
from .SeverityCounter import SeverityCounter
from typing import List


@dataclass
class TotalCounters:
    severity_counters: List[SeverityCounter]

    @classmethod
    def from_dict(cls, item: dict) -> "TotalCounters":
        return cls(
            severity_counters=[
                SeverityCounter.from_dict(sc)
                for sc in (item.get("severityCounters") or [])
            ]
        )
