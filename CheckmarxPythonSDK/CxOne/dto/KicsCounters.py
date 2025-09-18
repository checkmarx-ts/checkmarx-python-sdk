from dataclasses import dataclass
from typing import List


@dataclass
class KicsCounters:
    """
    Counters of KICS Engine
    Args:
        severity_counters (list of dict): array of the result count grouped by severity.
        status_counters (list of dict): array of the result count grouped by status.
        state_counters (list of dict): array of the counters grouped by state.
                        will be included only if the apply-predicates parameter is true
        severity_status_counters (list of dict): array of the counters grouped by severity and status.
                        will be included only if the include-severity-status parameter is true.
                        NOTICE: will not contain FIXED status.
        source_file_counters (list of dict):
        age_counters (list of dict): array of the result count grouped by age.
        total_counter (int): Total number of results
        files_scanned_counter (int): Number of files scanned
        platform_summary (list of dict): array of the result count grouped by platform.
        category_summary (list of dict): array of the result count grouped by category.
    """
    severity_counters: List[dict]
    status_counters: List[dict]
    state_counters: List[dict]
    severity_status_counters: List[dict]
    source_file_counters: List[dict]
    age_counters: List[dict]
    total_counter: int
    files_scanned_counter: List[dict]
    platform_summary: List[dict]
    category_summary: List[dict]


def construct_kics_counters(item):
    return KicsCounters(
        age_counters=item.get("ageCounters"),
        category_summary=item.get("categorySummary"),
        files_scanned_counter=item.get("filesScannedCounter"),
        platform_summary=item.get("platformSummary"),
        severity_counters=item.get("severityCounters"),
        severity_status_counters=item.get("severityStatusCounters"),
        state_counters=item.get("stateCounters"),
        status_counters=item.get("statusCounters"),
        total_counter=item.get("totalCounter"),
        source_file_counters=item.get("sourceFileCounters")
    )
