# encoding: utf-8
from dataclasses import dataclass
from typing import Optional
from .CxDataRetentionRequestStatusStage import CxDataRetentionRequestStatusStage


@dataclass
class CxDataRetentionRequestStatus:
    """
    data retention request status
    """

    id: Optional[int] = None
    stage: Optional[CxDataRetentionRequestStatusStage] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxDataRetentionRequestStatus":
        return cls(
            id=item.get("id"),
            stage=CxDataRetentionRequestStatusStage.from_dict(item.get("stage") or {}),
            link=item.get("link"),
        )
