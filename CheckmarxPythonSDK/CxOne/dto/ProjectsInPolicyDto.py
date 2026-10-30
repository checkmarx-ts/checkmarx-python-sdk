from dataclasses import dataclass, field, asdict
from typing import List, Optional

from .ProjectWebDto import ProjectWebDto


@dataclass
class ProjectsInPolicyDto:
    """Request body for assigning/removing projects on a policy.

    Used by PUT/DELETE /policies/projects/{policyId}.

    Attributes:
        projects (List[ProjectWebDto]): Projects to assign or remove.
        id (Optional[int]): The policy ID (also given in the URL path).
    """

    projects: List[ProjectWebDto] = field(default_factory=list)
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProjectsInPolicyDto":
        return cls(
            projects=[
                ProjectWebDto.from_dict(p) for p in (item.get("projects") or [])
            ],
            id=item.get("id"),
        )

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in asdict(
                self,
                dict_factory=lambda obj: {k: v for k, v in obj if v is not None},
            ).items()
            if v is not None
        }
