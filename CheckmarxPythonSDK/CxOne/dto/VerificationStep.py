from dataclasses import dataclass, field
from typing import List


@dataclass
class VerificationStep:
    """Allowed category values: REACHABILITY.
    Allowed status values: VERIFIED.
    """

    task: str = None
    category: str = None
    status: str = None
    thoughts: List[str] = field(default_factory=list)
    conclusion: str = ""
    usage_locations: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "VerificationStep":
        return cls(
            task=item.get("task"),
            category=item.get("category"),
            status=item.get("status"),
            thoughts=item.get("thoughts", []),
            conclusion=item.get("conclusion", ""),
            usage_locations=item.get("usage_locations", []),
        )
