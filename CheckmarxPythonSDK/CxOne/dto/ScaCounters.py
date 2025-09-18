from dataclasses import dataclass
from typing import List


@dataclass
class ScaCounters:
    """

    Attributes:
        severity_counters (list of dict): array of the result count grouped by severity.
        status_counters (list of dict): array of the result count grouped by status.
        state_counters (list of dict): array of the counters grouped by state. will be included only if the
                            apply-predicates parameter is true
        severity_status_counters (list of dict): array of the counters grouped by severity and status.
                        will be included only if the include-severity-status parameter is true.
                        NOTICE: will not contain FIXED status.
        source_file_counters (list of dict): array of the result count grouped by code source file.
        age_counters (list of dict): array of the result count grouped by age.
        total_counter (int): Total number of results
        file_scanned_counter (int):
    """

    severity_counters: List[dict]
    status_counters: List[dict]
    state_counters: List[dict]
    severity_status_counters: List[dict]
    source_file_counters: List[dict]
    age_counters: List[dict]
    total_counter: int
    file_scanned_counter: int


def construct_sca_counters(item):
    return ScaCounters(
        severity_counters=item.get("severityCounters"),
        status_counters=item.get("statusCounters"),
        state_counters=item.get("stateCounters"),
        severity_status_counters=item.get("severityStatusCounters"),
        source_file_counters=item.get("sourceFileCounters"),
        age_counters=item.get("ageCounters"),
        total_counter=item.get("totalCounter"),
        file_scanned_counter=item.get("filesScannedCounter")
    )
