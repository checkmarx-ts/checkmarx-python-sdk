from dataclasses import dataclass, field
from typing import List, Optional

from .PackageInfo import PackageInfo
from .PackageSuspectedMalware import PackageSuspectedMalware
from .PackageVulnerability import PackageVulnerability


@dataclass
class PackageRisk:
    """One entry in the response array of POST /api/v1/Packages/risks
    (SCA Data Hub service) -- vulnerability and malware risk data for
    one looked-up package version.

    Verified live: when package.status is "NotFound" (or similarly
    unresolvable), `vulnerabilities`/`suspected_malware` are absent
    from the response entirely rather than empty lists.
    """
    package: Optional[PackageInfo] = None
    vulnerabilities: List[PackageVulnerability] = field(default_factory=list)
    suspected_malware: List[PackageSuspectedMalware] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "PackageRisk":
        return cls(
            package=(
                PackageInfo.from_dict(item["package"])
                if item.get("package")
                else None
            ),
            vulnerabilities=[
                PackageVulnerability.from_dict(v)
                for v in (item.get("vulnerabilities") or [])
            ],
            suspected_malware=[
                PackageSuspectedMalware.from_dict(m)
                for m in (item.get("suspectedMalware") or [])
            ],
        )
