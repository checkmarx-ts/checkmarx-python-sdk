# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxIssueTrackingSystemField import CxIssueTrackingSystemField


@dataclass
class CxIssueTrackingSystemType:
    """
    one of issue types
    """

    id: Optional[str] = None
    name: Optional[str] = None
    sub_task: Optional[bool] = None
    fields: List[CxIssueTrackingSystemField] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxIssueTrackingSystemType":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            sub_task=item.get("subtask"),
            fields=[
                CxIssueTrackingSystemField.from_dict(f)
                for f in (item.get("fields") or [])
            ],
        )
