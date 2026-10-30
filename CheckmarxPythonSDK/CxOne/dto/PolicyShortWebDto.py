from dataclasses import dataclass
from typing import Optional


@dataclass
class PolicyShortWebDto:
    """A policy's ID and name only.

    Returned by POST /policies/v2 (create) and GET /policies/default.

    Attributes:
        id (Optional[int]): Policy ID.
        name (Optional[str]): Policy name.
    """

    id: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "PolicyShortWebDto":
        return cls(id=item.get("id"), name=item.get("name"))
