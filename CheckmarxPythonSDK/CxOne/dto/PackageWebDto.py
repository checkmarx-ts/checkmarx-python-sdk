from dataclasses import dataclass, field
from typing import List, Optional

from .VulnerabilityWebDto import VulnerabilityWebDto


@dataclass
class PackageWebDto:
    """An SCA package as referenced from a policy violation.

    Attributes:
        id (Optional[str]): Package ID.
        name (Optional[str]): Package name.
        version (Optional[str]): Package version.
        outdated (Optional[bool]): Whether a newer version is available.
        highVulnerabilityCount (Optional[int]): Count of high-severity vulnerabilities.
        mediumVulnerabilityCount (Optional[int]): Count of medium-severity vulnerabilities.
        packageState (Optional[str]): Current state of the package.
        vulnerabilities (List[VulnerabilityWebDto]): Vulnerabilities found in the package.
    """

    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    outdated: Optional[bool] = None
    highVulnerabilityCount: Optional[int] = None
    mediumVulnerabilityCount: Optional[int] = None
    packageState: Optional[str] = None
    vulnerabilities: List[VulnerabilityWebDto] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "PackageWebDto":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            version=item.get("version"),
            outdated=item.get("outdated"),
            highVulnerabilityCount=item.get("highVulnerabilityCount"),
            mediumVulnerabilityCount=item.get("mediumVulnerabilityCount"),
            packageState=item.get("packageState"),
            vulnerabilities=[
                VulnerabilityWebDto.from_dict(v)
                for v in (item.get("vulnerabilities") or [])
            ],
        )
