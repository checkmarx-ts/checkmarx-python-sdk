# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxDefineDataRetentionResponse:
    """
    define data retention response
    """

    id: Optional[int] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxDefineDataRetentionResponse":
        return cls(
            id=item.get("id"),
            link=item.get("link"),
        )
