from dataclasses import dataclass
from typing import List


@dataclass
class Project:
    id: str = None  # A unique identifier for the project. For 'upload' projects, a value must be entered.
    # For 'git' projects, this field can be empty and the repository URL will be designated as the project ID.
    name: str = None  # The project name
    groups: List[str] = None  # The groups authorized for this project
    repo_url: str = None  # The representative repository URL
    main_branch: str = None  # The Git main branch
    origin: str = None  # The origin of project
    created_at: str = None
    updated_at: str = None
    tags: dict = None
    criticality: int = 3  # minimum: 1 maximum: 5 default: 3 example: 3 Criticality level of the project

    def to_dict(self):
        data = {}
        if self.id:
            data.update({"id": self.id})
        if self.tags:
            data.update({"tags": self.tags})
        return data


def construct_project(item):
    return Project(
        id=item.get("id"),
        name=item.get("name"),
        groups=item.get("groups"),
        repo_url=item.get("repoUrl"),
        main_branch=item.get("mainBranch"),
        origin=item.get("origin"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        tags=item.get("tags"),
        criticality=item.get("criticality"),
    )
