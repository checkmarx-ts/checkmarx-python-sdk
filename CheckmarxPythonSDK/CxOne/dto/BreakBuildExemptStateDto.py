from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class BreakBuildExemptStateDto:
    """A result state that is exempt from breaking the build for a rule.

    Attributes:
        scanner (Optional[str]): The scanner the exemption applies to.
        ruleName (Optional[str]): The policy rule the exemption applies to.
        stateName (List[str]): Result states exempt from breaking the build.
    """

    scanner: Optional[str] = None
    ruleName: Optional[str] = None
    stateName: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "BreakBuildExemptStateDto":
        return cls(
            scanner=item.get("scanner"),
            ruleName=item.get("ruleName"),
            stateName=list(item.get("stateName") or []),
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
