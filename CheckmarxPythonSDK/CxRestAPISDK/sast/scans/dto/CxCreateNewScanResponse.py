# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxCreateNewScanResponse:
    """
    create new scan response
    """

    id: Optional[int] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxCreateNewScanResponse":
        return cls(
            id=item.get("id"),
            link=item.get("link"),
        )
