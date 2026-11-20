from dataclasses import dataclass
from typing import Optional


@dataclass
class ViolatingAssocProjectsWebDto:
    """Count of a policy's associated projects vs. those violating it.

    Attributes:
        assocProjects (Optional[int]): Number of projects the policy applies to.
        violating (Optional[int]): Number of those projects currently violating it.
    """

    assocProjects: Optional[int] = None
    violating: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ViolatingAssocProjectsWebDto":
        return cls(
            assocProjects=item.get("assocProjects"),
            violating=item.get("violating"),
        )
