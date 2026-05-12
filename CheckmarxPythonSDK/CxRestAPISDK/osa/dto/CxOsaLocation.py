# encoding: utf-8
from dataclasses import dataclass
from typing import Optional
from .CxOsaMatchType import CxOsaMatchType


@dataclass
class CxOsaLocation:
    """
    location
    """

    path: Optional[str] = None
    match_type: Optional[CxOsaMatchType] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaLocation":
        return cls(
            path=item.get("path"),
            match_type=CxOsaMatchType.from_dict(item.get("matchType") or {}),
        )
