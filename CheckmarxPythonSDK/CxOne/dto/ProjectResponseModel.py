from dataclasses import dataclass
from typing import List
from .TotalCounters import TotalCounters, construct_total_counters
from .EngineData import EngineData, construct_engine_data


@dataclass
class ProjectResponseModel:
    project_id: str = None  # The ID of the project.
    project_name: str = None  # The name of the project.
    source_origin: str = None  # The origin of the project source.
    last_scan_date: str = None  # The date of the last scan.
    source_type: str = None  # The type of project source.
    tags: dict = None  # A map of project tags.
    groups_ids: List[str] = None  # An array of group IDs associated with the project.
    risk_level: str = None  # The overall risk level of the project.
    repo_id: int = None  # The ID of the repository associated with the project.
    scm_repo_id: str = None  # The ID of the SCM repository associated with the project.
    total_counters: TotalCounters = None
    engines_data: List[EngineData] = None


def construct_project_response(item):
    return ProjectResponseModel(
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
        total_counters=construct_total_counters(item),
        engines_data=[
            construct_engine_data(engine_data) for engine_data in item.get("enginesData", [])
        ],
    )
