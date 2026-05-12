# encoding: utf-8
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CxSharedRemoteSourceSettingsResponse:

    paths: Optional[List[str]] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxSharedRemoteSourceSettingsResponse":
        from .CxLink import CxLink

        return cls(
            paths=item.get("paths"),
            link=CxLink.from_dict(item.get("link") or {}),
        )
