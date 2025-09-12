from dataclasses import dataclass
from typing import List


@dataclass
class ApiSecCounters:
    severity_counters: List[dict] = None
    status_counters: List[dict] = None
    state_counters: List[dict] = None
    custom_state_counters: List[dict] = None
    severity_status_counters: List[dict] = None
    source_file_counters: List[dict] = None
    age_counters: List[dict] = None
    risk_level: str = None
    files_scanned_counter: int = None
    total_counter: int = None
    api_sec_total: int = None


def construct_api_sec_counters(item):
    return ApiSecCounters(
        severity_counters=item.get("severityCounters"),
        status_counters=item.get("statusCounters"),
        state_counters=item.get("stateCounters"),
        custom_state_counters=item.get("customStateCounters"),
        severity_status_counters=item.get("severityStatusCounters"),
        source_file_counters=item.get("sourceFileCounters"),
        age_counters=item.get("ageCounters"),
        risk_level=item.get("riskLevel"),
        files_scanned_counter=item.get("filesScannedCounter"),
        total_counter=item.get("totalCounter"),
        api_sec_total=item.get("apiSecTotal"),
    )
