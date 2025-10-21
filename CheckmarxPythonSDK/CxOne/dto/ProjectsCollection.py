from dataclasses import dataclass
from typing import List
from .Project import Project, construct_project


@dataclass
class ProjectsCollection:
    total_count: int = None
    filtered_total_count: int = None
    projects: List[Project] = None


def construct_projects_collection(item):
    return ProjectsCollection(
            total_count=item.get("totalCount"),
            filtered_total_count=item.get("filteredTotalCount"),
            projects=[
                construct_project(project) for project in (item.get("projects") or [])
            ]
        )
