from dataclasses import dataclass, field
from typing import List, Optional

from .RuleViolatedWebDto import RuleViolatedWebDto


@dataclass
class ViolatedPolicyWebDto:
    """A policy that was violated by a scan, with the rules that triggered it.

    Attributes:
        policyName (Optional[str]): The violated policy's name.
        description (Optional[str]): The policy's description.
        tags (List[str]): The policy's tags.
        breakBuild (Optional[bool]): Whether this policy breaks the build.
        rulesViolated (List[RuleViolatedWebDto]): The rules that were violated.
    """

    policyName: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    breakBuild: Optional[bool] = None
    rulesViolated: List[RuleViolatedWebDto] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ViolatedPolicyWebDto":
        return cls(
            policyName=item.get("policyName"),
            description=item.get("description"),
            tags=list(item.get("tags") or []),
            breakBuild=item.get("breakBuild"),
            rulesViolated=[
                RuleViolatedWebDto.from_dict(r)
                for r in (item.get("rulesViolated") or [])
            ],
        )
