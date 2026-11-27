from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OrgCoverage:
    """Coverage of one SCM organization: how many of its repos are imported."""
    org_id: Optional[int] = None
    org_identity: Optional[str] = None
    scm_id: Optional[int] = None
    repos_count: Optional[int] = None
    imported_repos_count: Optional[int] = None
    kpi_number: Optional[float] = None  # percentage of repos imported
    admin_token: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "OrgCoverage":
        return cls(
            org_id=item.get("orgId"),
            org_identity=item.get("orgIdentity"),
            scm_id=item.get("scmId"),
            repos_count=item.get("reposCount"),
            imported_repos_count=item.get("importedReposCount"),
            kpi_number=item.get("kpiNumber"),
            admin_token=item.get("adminToken"),
        )


@dataclass
class ScmCoverage:
    """Coverage of one SCM instance (GET /api/discovery/v2/orgs/coverage)."""
    scm_id: Optional[int] = None
    type: Optional[str] = None  # github, gitlab, azure, bitbucket, ...
    display: Optional[str] = None
    on_prem: Optional[bool] = None
    total_repos_count: Optional[int] = None
    total_imported_repos_count: Optional[int] = None
    total_kpi_number: Optional[float] = None
    org_coverage_list: List[OrgCoverage] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ScmCoverage":
        return cls(
            scm_id=item.get("scmId"),
            type=item.get("type"),
            display=item.get("display"),
            on_prem=item.get("onPrem"),
            total_repos_count=item.get("totalReposCount"),
            total_imported_repos_count=item.get("totalImportedReposCount"),
            total_kpi_number=item.get("totalKpiNumber"),
            org_coverage_list=[
                OrgCoverage.from_dict(o)
                for o in (item.get("orgCoverageDtoList") or [])
            ],
        )
