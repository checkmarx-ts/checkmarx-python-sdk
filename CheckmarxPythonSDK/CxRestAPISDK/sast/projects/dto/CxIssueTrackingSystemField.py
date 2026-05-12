# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxIssueTrackingSystemFieldAllowedValue import (
    CxIssueTrackingSystemFieldAllowedValue,
)


@dataclass
class CxIssueTrackingSystemField:
    """
    field
    """

    id: Optional[int] = None
    name: Optional[str] = None
    multiple: Optional[bool] = None
    required: Optional[bool] = None
    supported: Optional[bool] = None
    allowed_values: List[CxIssueTrackingSystemFieldAllowedValue] = field(
        default_factory=list
    )

    @classmethod
    def from_dict(cls, item: dict) -> "CxIssueTrackingSystemField":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            multiple=item.get("multiple"),
            required=item.get("required"),
            supported=item.get("supported"),
            allowed_values=[
                CxIssueTrackingSystemFieldAllowedValue.from_dict(v)
                for v in (item.get("allowedValues") or [])
            ],
        )
