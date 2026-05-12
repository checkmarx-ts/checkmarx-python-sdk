from dataclasses import dataclass
from typing import List


@dataclass
class ScaContainersCounters:
    total_packages_counter: int = None
    total_vulnerabilities_counter: int = None
    severity_vulnerabilities_counters: List[dict] = None
    state_vulnerabilities_counters: List[dict] = None
    status_vulnerabilities_counters: List[dict] = None
    age_vulnerabilities_counters: List[dict] = None
    package_vulnerabilities_counters: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScaContainersCounters":
        return cls(
            total_packages_counter=item.get("totalPackagesCounter"),
            total_vulnerabilities_counter=item.get("totalVulnerabilitiesCounter"),
            severity_vulnerabilities_counters=item.get(
                "severityVulnerabilitiesCounters"
            ),
            state_vulnerabilities_counters=item.get("stateVulnerabilitiesCounters"),
            status_vulnerabilities_counters=item.get("statusVulnerabilitiesCounters"),
            age_vulnerabilities_counters=item.get("ageVulnerabilitiesCounters"),
            package_vulnerabilities_counters=item.get("packageVulnerabilitiesCounters"),
        )
