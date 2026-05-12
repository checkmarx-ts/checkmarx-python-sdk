from dataclasses import dataclass
from typing import List


@dataclass
class KicsCounters:
    severity_counters: List[dict] = None
    status_counters: List[dict] = None
    state_counters: List[dict] = None
    severity_status_counters: List[dict] = None
    source_file_counters: List[dict] = None
    age_counters: List[dict] = None
    total_counter: int = None
    files_scanned_counter: List[dict] = None
    platform_summary: List[dict] = None
    category_summary: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "KicsCounters":
        return cls(
            age_counters=item.get("ageCounters"),
            category_summary=item.get("categorySummary"),
            files_scanned_counter=item.get("filesScannedCounter"),
            platform_summary=item.get("platformSummary"),
            severity_counters=item.get("severityCounters"),
            severity_status_counters=item.get("severityStatusCounters"),
            state_counters=item.get("stateCounters"),
            status_counters=item.get("statusCounters"),
            total_counter=item.get("totalCounter"),
            source_file_counters=item.get("sourceFileCounters"),
        )
