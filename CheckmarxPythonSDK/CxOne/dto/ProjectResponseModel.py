from dataclasses import dataclass
from typing import List
from .TotalCounters import TotalCounters
from .EngineData import EngineData


@dataclass
class ProjectResponseModel:
    project_id: str = None
    project_name: str = None
    source_origin: str = None
    last_scan_date: str = None
    source_type: str = None
    tags: dict = None
    groups_ids: List[str] = None
    risk_level: str = None
    repo_id: int = None
    scm_repo_id: str = None
    total_counters: TotalCounters = None
    engines_data: List[EngineData] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProjectResponseModel":
        return cls(
            project_id=item.get("projectId"),
            project_name=item.get("projectName"),
            source_origin=item.get("sourceOrigin"),
            last_scan_date=item.get("lastScanDate"),
            source_type=item.get("sourceType"),
            tags=item.get("tags"),
            groups_ids=item.get("groupIds"),
            risk_level=item.get("riskLevel"),
            repo_id=item.get("repoId"),
            scm_repo_id=item.get("scmRepoId"),
            total_counters=TotalCounters.from_dict(item),
            engines_data=[
                EngineData.from_dict(e) for e in (item.get("enginesData") or [])
            ],
        )
