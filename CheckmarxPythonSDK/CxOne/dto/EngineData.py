from dataclasses import dataclass
from typing import List
from .SeverityCounter import SeverityCounter


@dataclass
class EngineData:
    engine: str = None
    risk_level: str = None
    last_scan_id: str = None
    severity_counters: List[SeverityCounter] = None

    @classmethod
    def from_dict(cls, item: dict) -> "EngineData":
        return cls(
            engine=item.get("engine"),
            risk_level=item.get("riskLevel"),
            last_scan_id=item.get("lastScanId"),
            severity_counters=[
                SeverityCounter.from_dict(sc)
                for sc in (item.get("severityCounters") or [])
            ],
        )
