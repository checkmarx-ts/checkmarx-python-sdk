from dataclasses import dataclass, field
from typing import List, Optional

from .VerificationStep import VerificationStep
from .RepositoryInfo import RepositoryInfo


@dataclass
class ReasoningTrace:
    verification_steps: List[VerificationStep] = field(default_factory=list)
    repository_info: Optional[RepositoryInfo] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ReasoningTrace":
        return cls(
            verification_steps=[
                VerificationStep.from_dict(s)
                for s in item.get("verification_steps", [])
            ],
            repository_info=(
                RepositoryInfo.from_dict(item["repository_info"])
                if item.get("repository_info")
                else None
            ),
        )
