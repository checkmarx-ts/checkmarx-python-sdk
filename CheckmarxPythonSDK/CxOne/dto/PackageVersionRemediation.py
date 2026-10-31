from dataclasses import dataclass
from typing import Optional

from .RemediationVersionCounts import RemediationVersionCounts


@dataclass
class PackageVersionRemediation:
    """PackageInfo.remediation -- returned when IncludeVersionRemediation
    is true. Suggests upgrade targets and their resulting vuln counts.
    """
    latest: Optional[RemediationVersionCounts] = None
    nearest: Optional[RemediationVersionCounts] = None
    current: Optional[RemediationVersionCounts] = None

    @classmethod
    def from_dict(cls, item: dict) -> "PackageVersionRemediation":
        return cls(
            latest=(
                RemediationVersionCounts.from_dict(item["latest"])
                if item.get("latest")
                else None
            ),
            nearest=(
                RemediationVersionCounts.from_dict(item["nearest"])
                if item.get("nearest")
                else None
            ),
            current=(
                RemediationVersionCounts.from_dict(item["current"])
                if item.get("current")
                else None
            ),
        )
