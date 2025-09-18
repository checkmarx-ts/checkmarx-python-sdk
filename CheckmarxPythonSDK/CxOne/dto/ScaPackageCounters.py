from dataclasses import dataclass
from typing import List


@dataclass
class ScaPackageCounters:
    """

    Args:
        severity_counters (list of dict):
        status_counters (list of dict):
        state_counters (list of dict):
        severity_status_counters (list of dict):
        source_file_counters (list of dict):
        age_counters (list of dict):
        total_counter (int):
        files_scanned_counter (int):
        outdated_counter (int):
        risk_level_counters (list of dict):
        license_counters (list of dict):
        package_counters (list of dict):
    """

    severity_counters: List[dict]
    status_counters: List[dict]
    state_counters: List[dict]
    severity_status_counters: List[dict]
    source_file_counters: List[dict]
    age_counters: List[dict]
    total_counter: int
    files_scanned_counter: List[dict]
    outdated_counter: int
    risk_level_counters: List[dict]
    license_counters: List[dict]
    package_counters: List[dict]


def construct_sca_package_counters(item):
    return ScaPackageCounters(
        severity_counters=item.get("severityCounters"),
        status_counters=item.get("statusCounters"),
        state_counters=item.get("stateCounters"),
        severity_status_counters=item.get("severityStatusCounters"),
        source_file_counters=item.get("sourceFileCounters"),
        age_counters=item.get("ageCounters"),
        total_counter=item.get("totalCounter"),
        files_scanned_counter=item.get("filesScannedCounter"),
        outdated_counter=item.get("outdatedCounter"),
        risk_level_counters=item.get("riskLevelCounters"),
        license_counters=item.get("licenseCounters"),
        package_counters=item.get("packageCounters")
    )
