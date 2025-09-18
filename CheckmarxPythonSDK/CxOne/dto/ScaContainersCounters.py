from dataclasses import dataclass
from typing import List


@dataclass
class ScaContainersCounters:
    """

    Args:
        total_packages_counter (int):
        total_vulnerabilities_counter (int):
        severity_vulnerabilities_counters (list of dict):
        state_vulnerabilities_counters (list of dict):
        status_vulnerabilities_counters (list of dict):
        age_vulnerabilities_counters (list of dict):
        package_vulnerabilities_counters (list of dict):
    """

    total_packages_counter: int
    total_vulnerabilities_counter: int
    severity_vulnerabilities_counters: List[dict]
    state_vulnerabilities_counters: List[dict]
    status_vulnerabilities_counters: List[dict]
    age_vulnerabilities_counters: List[dict]
    package_vulnerabilities_counters: List[dict]


def construct_sca_containers_counters(item):
    return ScaContainersCounters(
        total_packages_counter=item.get("totalPackagesCounter"),
        total_vulnerabilities_counter=item.get("totalVulnerabilitiesCounter"),
        severity_vulnerabilities_counters=item.get("severityVulnerabilitiesCounters"),
        state_vulnerabilities_counters=item.get("stateVulnerabilitiesCounters"),
        status_vulnerabilities_counters=item.get("statusVulnerabilitiesCounters"),
        age_vulnerabilities_counters=item.get("ageVulnerabilitiesCounters"),
        package_vulnerabilities_counters=item.get("packageVulnerabilitiesCounters")
    )
