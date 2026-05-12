# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxOsaSummaryReport:
    """
    osa report
    """

    total_libraries: Optional[int] = None
    high_vulnerability_libraries: Optional[int] = None
    medium_vulnerability_libraries: Optional[int] = None
    low_vulnerability_libraries: Optional[int] = None
    non_vulnerable_libraries: Optional[int] = None
    vulnerable_and_updated: Optional[int] = None
    vulnerable_and_outdated: Optional[int] = None
    vulnerability_score: Optional[float] = None
    total_high_vulnerabilities: Optional[int] = None
    total_medium_vulnerabilities: Optional[int] = None
    total_low_vulnerabilities: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaSummaryReport":
        return cls(
            total_libraries=item.get("totalLibraries"),
            high_vulnerability_libraries=item.get("highVulnerabilityLibraries"),
            medium_vulnerability_libraries=item.get("mediumVulnerabilityLibraries"),
            low_vulnerability_libraries=item.get("lowVulnerabilityLibraries"),
            non_vulnerable_libraries=item.get("nonVulnerableLibraries"),
            vulnerable_and_updated=item.get("vulnerableAndUpdated"),
            vulnerable_and_outdated=item.get("vulnerableAndOutdated"),
            vulnerability_score=item.get("vulnerabilityScore"),
            total_high_vulnerabilities=item.get("totalHighVulnerabilities"),
            total_medium_vulnerabilities=item.get("totalMediumVulnerabilities"),
            total_low_vulnerabilities=item.get("totalLowVulnerabilities"),
        )
