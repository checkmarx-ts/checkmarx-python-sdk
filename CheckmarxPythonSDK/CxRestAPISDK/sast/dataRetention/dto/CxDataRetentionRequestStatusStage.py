# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxDataRetentionRequestStatusStage:
    """
    data retention request status stage
    """

    id: Optional[int] = None
    value: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxDataRetentionRequestStatusStage":
        return cls(
            id=item.get("id"),
            value=item.get("value"),
        )
