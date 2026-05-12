# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxIssueTrackingSystemType import CxIssueTrackingSystemType


@dataclass
class CxIssueTrackingSystemDetail:
    """
    issue tracking system detail
    """

    id: Optional[int] = None
    name: Optional[str] = None
    issue_types: List[CxIssueTrackingSystemType] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxIssueTrackingSystemDetail":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            issue_types=[
                CxIssueTrackingSystemType.from_dict(t)
                for t in (item.get("issueTypes") or [])
            ],
        )
