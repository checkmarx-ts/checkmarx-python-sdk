from dataclasses import dataclass
from typing import List
from .SeverityCounter import SeverityCounter, construct_severity_counter


@dataclass
class EngineData:
    engine: str = None  # The name of the scanning engine.
    risk_level: str = None  # The risk level reported by the engine.
    last_scan_id: str = None  # The ID of the last scan performed by the engine.
    severity_counters: List[SeverityCounter] = None


def construct_engine_data(item):
    return EngineData(
        engine=item.get("engine"),
        risk_level=item.get("riskLevel"),
        last_scan_id=item.get("lastScanId"),
        severity_counters=[
            construct_severity_counter(severity_counter) for severity_counter in item.get("severityCounters", [])
        ]
    )
