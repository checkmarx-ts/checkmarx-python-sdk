from dataclasses import dataclass
from typing import List


@dataclass
class Project:
    id: str = None
    name: str = None
    application_ids: List[str] = None
    groups: List[str] = None
    repo_url: str = None
    main_branch: str = None
    origin: str = None
    repo_id: int = None
    scm_repo_id: str = None
    created_at: str = None
    updated_at: str = None
    tags: dict = None
    criticality: int = 3

    @classmethod
    def from_dict(cls, item: dict) -> "Project":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            application_ids=item.get("applicationIds"),
            groups=item.get("groups"),
            repo_url=item.get("repoUrl"),
            main_branch=item.get("mainBranch"),
            origin=item.get("origin"),
            repo_id=item.get("repoId"),
            scm_repo_id=item.get("scmRepoId"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
            tags=item.get("tags"),
            criticality=item.get("criticality"),
        )
