from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from .BreakBuildExemptStateDto import BreakBuildExemptStateDto
from .ProjectWebDto import ProjectWebDto
from .ViolatingAssocProjectsWebDto import ViolatingAssocProjectsWebDto


@dataclass
class PolicyWebDto:
    """A Policy Manager policy.

    Used both as the request body for create/update and as the response
    shape for get/list.

    Attributes:
        id (Optional[int]): Policy ID. Only set on existing policies.
        name (str): Policy name (1-255 chars). Required.
        description (Optional[str]): Policy description (0-2500 chars).
        isActivated (Optional[bool]): Whether the policy is active.
        tags (List[str]): Up to 50 unique tags.
        breakBuild (Optional[bool]): Whether a violation breaks the build.
        pinPolicy (Optional[bool]): Whether the policy is pinned.
        lastViolated (Optional[str]): When the policy was last violated (date-time).
        updatedAt (Optional[str]): Last update time (date-time).
        projects (List[ProjectWebDto]): Projects the policy is assigned to.
        netNewBreakBuild (Optional[bool]): Whether only net-new violations break the build.
        type (Optional[str]): Policy type. Values: NET_NEW, ENGINES_RULES.
        allScannersSeverities (List[str]): Severities applied across all scanners.
            Values: CRITICAL, HIGH, MEDIUM, LOW, INFO.
        violatingAssocProjects (Optional[ViolatingAssocProjectsWebDto]):
            Count of associated vs. violating projects.
        netNewScannerMode (Optional[str]): Net-new scanner mode. Values:
            ALL_SCANNERS, BY_SCANNER.
        scannerSeverities (Dict[str, List[str]]): Per-scanner severity lists
            when netNewScannerMode is BY_SCANNER.
        breakBuildExemptStates (List[BreakBuildExemptStateDto]): Result
            states exempt from breaking the build, per rule/scanner.
        defaultPolicy (Optional[bool]): Whether this is the tenant's default policy.
    """

    name: str
    id: Optional[int] = None
    description: Optional[str] = None
    isActivated: Optional[bool] = None
    tags: List[str] = field(default_factory=list)
    breakBuild: Optional[bool] = None
    pinPolicy: Optional[bool] = None
    lastViolated: Optional[str] = None
    updatedAt: Optional[str] = None
    projects: List[ProjectWebDto] = field(default_factory=list)
    netNewBreakBuild: Optional[bool] = None
    type: Optional[str] = None
    allScannersSeverities: List[str] = field(default_factory=list)
    violatingAssocProjects: Optional[ViolatingAssocProjectsWebDto] = None
    netNewScannerMode: Optional[str] = None
    scannerSeverities: Dict[str, List[str]] = field(default_factory=dict)
    breakBuildExemptStates: List[BreakBuildExemptStateDto] = field(default_factory=list)
    defaultPolicy: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "PolicyWebDto":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            isActivated=item.get("isActivated"),
            tags=list(item.get("tags") or []),
            breakBuild=item.get("breakBuild"),
            pinPolicy=item.get("pinPolicy"),
            lastViolated=item.get("lastViolated"),
            updatedAt=item.get("updatedAt"),
            projects=[
                ProjectWebDto.from_dict(p) for p in (item.get("projects") or [])
            ],
            netNewBreakBuild=item.get("netNewBreakBuild"),
            type=item.get("type"),
            allScannersSeverities=list(item.get("allScannersSeverities") or []),
            violatingAssocProjects=(
                ViolatingAssocProjectsWebDto.from_dict(item["violatingAssocProjects"])
                if item.get("violatingAssocProjects")
                else None
            ),
            netNewScannerMode=item.get("netNewScannerMode"),
            scannerSeverities=dict(item.get("scannerSeverities") or {}),
            breakBuildExemptStates=[
                BreakBuildExemptStateDto.from_dict(s)
                for s in (item.get("breakBuildExemptStates") or [])
            ],
            defaultPolicy=item.get("defaultPolicy"),
        )

    def to_dict(self) -> dict:
        # asdict() recursively converts nested dataclasses (projects,
        # violatingAssocProjects, breakBuildExemptStates) to plain dicts;
        # dict_factory drops None values at every nesting level.
        return {
            k: v
            for k, v in asdict(
                self,
                dict_factory=lambda obj: {k: v for k, v in obj if v is not None},
            ).items()
            if v is not None
        }
