# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxIssueTrackingSystem:
    """
    issue tracking system
    """

    id: Optional[int] = None
    name: Optional[str] = None
    tracking_system_type: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxIssueTrackingSystem":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            tracking_system_type=item.get("type"),
            url=item.get("url"),
        )
