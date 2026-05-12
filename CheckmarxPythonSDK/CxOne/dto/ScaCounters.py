from dataclasses import dataclass
from typing import List


@dataclass
class ScaCounters:
    severity_counters: List[dict] = None
    status_counters: List[dict] = None
    state_counters: List[dict] = None
    severity_status_counters: List[dict] = None
    source_file_counters: List[dict] = None
    age_counters: List[dict] = None
    total_counter: int = None
    file_scanned_counter: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScaCounters":
        return cls(
            severity_counters=item.get("severityCounters"),
            status_counters=item.get("statusCounters"),
            state_counters=item.get("stateCounters"),
            severity_status_counters=item.get("severityStatusCounters"),
            source_file_counters=item.get("sourceFileCounters"),
            age_counters=item.get("ageCounters"),
            total_counter=item.get("totalCounter"),
            file_scanned_counter=item.get("filesScannedCounter"),
        )
