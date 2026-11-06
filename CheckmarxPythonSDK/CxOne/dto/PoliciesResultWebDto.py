from dataclasses import dataclass, field
from typing import List, Optional

from .EvaluatedPolicyWebDto import EvaluatedPolicyWebDto


@dataclass
class PoliciesResultWebDto:
    """Response from GET /evaluation (policy evaluation for a scan/project).

    Attributes:
        status (Optional[str]): Overall evaluation status. Values:
            COMPLETED, NONE, EVALUATING.
        breakBuild (Optional[bool]): Whether any evaluated policy breaks the build.
        policies (List[EvaluatedPolicyWebDto]): Per-policy evaluation results.
    """

    status: Optional[str] = None
    breakBuild: Optional[bool] = None
    policies: List[EvaluatedPolicyWebDto] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "PoliciesResultWebDto":
        return cls(
            status=item.get("status"),
            breakBuild=item.get("breakBuild"),
            policies=[
                EvaluatedPolicyWebDto.from_dict(p)
                for p in (item.get("policies") or [])
            ],
        )
