from dataclasses import dataclass, field
from typing import List, Optional

from .FindingsWebDto import FindingsWebDto
from .PackageWebDto import PackageWebDto


@dataclass
class RuleViolatedWebDto:
    """A single policy rule that was violated.

    Attributes:
        ruleName (Optional[str]): The violated rule's name.
        scanner (Optional[str]): The scanner that produced the violation.
        packages (List[PackageWebDto]): SCA packages involved, if any.
        findings (List[FindingsWebDto]): SAST/IaC findings involved, if any.
    """

    ruleName: Optional[str] = None
    scanner: Optional[str] = None
    packages: List[PackageWebDto] = field(default_factory=list)
    findings: List[FindingsWebDto] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "RuleViolatedWebDto":
        return cls(
            ruleName=item.get("ruleName"),
            scanner=item.get("scanner"),
            packages=[
                PackageWebDto.from_dict(p) for p in (item.get("packages") or [])
            ],
            findings=[
                FindingsWebDto.from_dict(f) for f in (item.get("findings") or [])
            ],
        )
