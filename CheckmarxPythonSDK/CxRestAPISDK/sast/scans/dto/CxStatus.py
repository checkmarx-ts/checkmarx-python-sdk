# encoding: utf-8
from dataclasses import dataclass
from typing import Optional
from .CxStatusDetail import CxStatusDetail


@dataclass
class CxStatus:
    """
    scan status
    """

    id: Optional[int] = None
    name: Optional[str] = None
    details: Optional[CxStatusDetail] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxStatus":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            details=CxStatusDetail.from_dict(item.get("details") or {}),
        )
