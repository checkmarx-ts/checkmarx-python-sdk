# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanType:
    """
    scan type
    """

    id: Optional[int] = None
    value: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanType":
        return cls(
            id=item.get("id"),
            value=item.get("value"),
        )
