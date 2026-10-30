from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ViolationDetailsDTO:
    """Describes the policy rule an incident's results violated.

    Attributes:
        policyName (Optional[str]): Name of the violated policy.
        ruleName (Optional[str]): Name of the violated rule.
        engine (Optional[str]): The scanner engine that produced the violation.
        conditions (List[str]): The rule's conditions.
        breakBuild (Optional[bool]): Whether this violation breaks the build.
    """

    policyName: Optional[str] = None
    ruleName: Optional[str] = None
    engine: Optional[str] = None
    conditions: List[str] = field(default_factory=list)
    breakBuild: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ViolationDetailsDTO":
        return cls(
            policyName=item.get("policyName"),
            ruleName=item.get("ruleName"),
            engine=item.get("engine"),
            conditions=list(item.get("conditions") or []),
            breakBuild=item.get("breakBuild"),
        )
