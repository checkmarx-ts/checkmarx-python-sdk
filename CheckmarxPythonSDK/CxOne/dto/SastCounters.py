from dataclasses import dataclass
from typing import List


@dataclass
class SastCounters:
    """

    Args:
        queries_counters (list of dict): array of the counters grouped by query name.
                                    will be included only if the include-queries parameter is true.
        sink_file_counters (list of dict): array of the result count grouped by code sink file.
        language_counters (list of dict): array of the result count grouped by language.
        compliance_counters (list of dict): array of the result count grouped by compliance
        severity_counters (list of dict): array of the result count grouped by severity.
        status_counters (list of dict): array of the result count grouped by status.
        state_counters (list of dict): array of the counters grouped by state. will be included only if the
                    apply-predicates parameter is true
        severity_status_counters (list of dict): array of the counters grouped by severity and status. will be
                    included only if the include-severity-status parameter is true.
                    NOTICE: will not contain FIXED status.
        source_file_counters (list of dict): array of the result count grouped by code source file.
        age_counters (list of dict): array of the result count grouped by age.
        total_counter (int): Total number of results
        file_scanned_counter (int):
    """
    queries_counters: List[dict] = None
    sink_file_counters: List[dict] = None,
    language_counters: List[dict] = None
    compliance_counters: List[dict] = None
    severity_counters: List[dict] = None
    status_counters: List[dict] = None
    state_counters: List[dict] = None
    severity_status_counters: List[dict] = None,
    source_file_counters: List[dict] = None
    age_counters: List[dict] = None
    total_counter: int = None
    file_scanned_counter: int = None


def construct_sast_counters(item):
    return SastCounters(
        queries_counters=item.get("queriesCounters"),
        sink_file_counters=item.get("sinkFileCounters"),
        language_counters=item.get("languageCounters"),
        compliance_counters=item.get("complianceCounters"),
        severity_counters=item.get("severityCounters"),
        status_counters=item.get("statusCounters"),
        state_counters=item.get("stateCounters"),
        severity_status_counters=item.get("severityStatusCounters"),
        source_file_counters=item.get("sourceFileCounters"),
        age_counters=item.get("ageCounters"),
        total_counter=item.get("totalCounter"),
        file_scanned_counter=item.get("filesScannedCounter")
    )
