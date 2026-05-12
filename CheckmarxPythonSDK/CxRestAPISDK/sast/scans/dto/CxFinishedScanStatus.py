# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxFinishedScanStatus:
    """
    finished scan status
    """

    id: Optional[int] = None
    value: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxFinishedScanStatus":
        return cls(
            id=item.get("id"),
            value=item.get("value"),
        )
