from dataclasses import dataclass
from typing import List


@dataclass
class ScaPackageCounters:
    severity_counters: List[dict] = None
    status_counters: List[dict] = None
    state_counters: List[dict] = None
    severity_status_counters: List[dict] = None
    source_file_counters: List[dict] = None
    age_counters: List[dict] = None
    total_counter: int = None
    files_scanned_counter: List[dict] = None
    outdated_counter: int = None
    risk_level_counters: List[dict] = None
    license_counters: List[dict] = None
    package_counters: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScaPackageCounters":
        return cls(
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
            package_counters=item.get("packageCounters"),
        )
