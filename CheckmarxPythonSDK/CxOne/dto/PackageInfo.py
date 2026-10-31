from dataclasses import dataclass
from typing import Optional

from .PackageVersionRemediation import PackageVersionRemediation


@dataclass
class PackageInfo:
    """PackageRisk.package -- identifies the looked-up package version
    and carries its status/risk-summary fields.

    package_reliability/runtime_behavior/contributor_reputation are
    undocumented in the public spec and observed only sparsely on the
    live tenant (present for some packages, absent for others) --
    kept as plain optional ints rather than guessing at a richer shape.
    """
    status: Optional[str] = None  # Ok, NotFound, UnsupportedPackageType, MissingVersion, InvalidPurl
    is_deprecated: Optional[bool] = None
    is_prerelease: Optional[bool] = None
    release_date: Optional[str] = None
    is_latest: Optional[bool] = None
    is_latest_prerelease: Optional[bool] = None
    remediation: Optional[PackageVersionRemediation] = None
    package_reliability: Optional[int] = None
    runtime_behavior: Optional[int] = None
    contributor_reputation: Optional[int] = None
    type: Optional[str] = None
    module_type: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    purl: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "PackageInfo":
        return cls(
            status=item.get("status"),
            is_deprecated=item.get("isDeprecated"),
            is_prerelease=item.get("isPrerelease"),
            release_date=item.get("releaseDate"),
            is_latest=item.get("isLatest"),
            is_latest_prerelease=item.get("isLatestPrerelease"),
            remediation=(
                PackageVersionRemediation.from_dict(item["remediation"])
                if item.get("remediation")
                else None
            ),
            package_reliability=item.get("packageReliability"),
            runtime_behavior=item.get("runtimeBehavior"),
            contributor_reputation=item.get("contributorReputation"),
            type=item.get("type"),
            module_type=item.get("moduleType"),
            name=item.get("name"),
            version=item.get("version"),
            purl=item.get("purl"),
        )
