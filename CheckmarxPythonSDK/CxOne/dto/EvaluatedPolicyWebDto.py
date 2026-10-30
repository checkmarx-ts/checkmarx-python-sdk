from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EvaluatedPolicyWebDto:
    """A single policy's evaluation result for one scan/project.

    Attributes:
        policyName (Optional[str]): The evaluated policy's name.
        description (Optional[str]): The policy's description.
        rulesViolated (List[str]): Names of rules that were violated.
        tags (List[str]): The policy's tags.
        breakBuild (Optional[bool]): Whether this policy breaks the build.
        status (Optional[str]): Evaluation status. Values: PASSED, FAILED.
    """

    policyName: Optional[str] = None
    description: Optional[str] = None
    rulesViolated: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    breakBuild: Optional[bool] = None
    status: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "EvaluatedPolicyWebDto":
        return cls(
            policyName=item.get("policyName"),
            description=item.get("description"),
            rulesViolated=list(item.get("rulesViolated") or []),
            tags=list(item.get("tags") or []),
            breakBuild=item.get("breakBuild"),
            status=item.get("status"),
        )
