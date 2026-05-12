# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxIssueTrackingSystemFieldAllowedValue:
    """
    allowed value
    """

    id: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxIssueTrackingSystemFieldAllowedValue":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
        )
