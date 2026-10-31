from dataclasses import dataclass
from typing import Optional


@dataclass
class RemediationVersionCounts:
    """Per-severity vulnerability counts for one version referenced in
    PackageVersionRemediation (latest/nearest/current).
    """
    version: Optional[str] = None
    critical_vulnerabilities: Optional[int] = None
    high_vulnerabilities: Optional[int] = None
    medium_vulnerabilities: Optional[int] = None
    low_vulnerabilities: Optional[int] = None
    none_vulnerabilities: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RemediationVersionCounts":
        return cls(
            version=item.get("version"),
            critical_vulnerabilities=item.get("criticalVulnerabilities"),
            high_vulnerabilities=item.get("highVulnerabilities"),
            medium_vulnerabilities=item.get("mediumVulnerabilities"),
            low_vulnerabilities=item.get("lowVulnerabilities"),
            none_vulnerabilities=item.get("noneVulnerabilities"),
        )
