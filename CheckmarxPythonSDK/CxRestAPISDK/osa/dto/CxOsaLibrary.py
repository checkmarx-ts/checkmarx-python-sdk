# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxOsaMatchType import CxOsaMatchType
from .CxOsaSeverity import CxOsaSeverity
from .CxOsaLocation import CxOsaLocation


@dataclass
class CxOsaLibrary:
    """
    osa libraries
    """

    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    release_date: Optional[str] = None
    high_unique_vulnerability_count: Optional[int] = None
    medium_unique_vulnerability_count: Optional[int] = None
    low_unique_vulnerability_count: Optional[int] = None
    not_exploitable_vulnerability_count: Optional[int] = None
    newest_version: Optional[str] = None
    newest_version_release_date: Optional[str] = None
    number_of_versions_since_last_update: Optional[int] = None
    confidence_level: Optional[int] = None
    match_type: Optional[CxOsaMatchType] = None
    licenses: Optional[list] = None
    outdated: Optional[bool] = None
    severity: Optional[CxOsaSeverity] = None
    risk_score: Optional[float] = None
    locations: List[CxOsaLocation] = field(default_factory=list)
    code_usage_status: Optional[str] = None
    code_reference_count: Optional[int] = None
    package_repository: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaLibrary":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            version=item.get("version"),
            release_date=item.get("releaseDate"),
            high_unique_vulnerability_count=item.get("highUniqueVulnerabilityCount"),
            medium_unique_vulnerability_count=item.get(
                "mediumUniqueVulnerabilityCount"
            ),
            low_unique_vulnerability_count=item.get("lowUniqueVulnerabilityCount"),
            not_exploitable_vulnerability_count=item.get(
                "notExploitableVulnerabilityCount"
            ),
            newest_version=item.get("newestVersion"),
            newest_version_release_date=item.get("newestVersionReleaseDate"),
            number_of_versions_since_last_update=item.get(
                "numberOfVersionsSinceLastUpdate"
            ),
            confidence_level=item.get("confidenceLevel"),
            match_type=CxOsaMatchType.from_dict(item.get("matchType") or {}),
            licenses=item.get("licenses"),
            outdated=item.get("outdated"),
            severity=CxOsaSeverity.from_dict(item.get("severity") or {}),
            risk_score=item.get("riskScore"),
            locations=[
                CxOsaLocation.from_dict(loc) for loc in (item.get("locations") or [])
            ],
            code_usage_status=item.get("codeUsageStatus"),
            code_reference_count=item.get("codeReferenceCount"),
            package_repository=item.get("packageRepository"),
        )
