from dataclasses import dataclass
from .ProjectResponseModel import ProjectResponseModel
from typing import List


@dataclass
class ProjectResponseCollection:
    total_count: int = None
    projects: List[ProjectResponseModel] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProjectResponseCollection":
        return cls(
            total_count=item.get("totalCount"),
            projects=[
                ProjectResponseModel.from_dict(p) for p in (item.get("projects") or [])
            ],
        )
