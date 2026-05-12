from dataclasses import dataclass
from typing import List
from .Project import Project


@dataclass
class ProjectsCollection:
    total_count: int = None
    filtered_total_count: int = None
    projects: List[Project] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProjectsCollection":
        return cls(
            total_count=item.get("totalCount"),
            filtered_total_count=item.get("filteredTotalCount"),
            projects=[Project.from_dict(p) for p in (item.get("projects") or [])],
        )
