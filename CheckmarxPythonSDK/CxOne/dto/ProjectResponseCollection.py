from dataclasses import dataclass
from .ProjectResponseModel import ProjectResponseModel, construct_project_response
from typing import List


@dataclass
class ProjectResponseCollection:
    total_count: int = None  # The total number of projects.
    projects: List[ProjectResponseModel] = None


def construct_project_response_collection(item):
    return ProjectResponseCollection(
        total_count=item.get("totalCount"),
        projects=[
            construct_project_response(project_response) for project_response in item.get("projects", [])
        ],
    )
