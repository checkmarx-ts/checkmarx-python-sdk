# encoding: utf-8
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CxPreset:
    """
    the queries set
    """

    id: Optional[int] = None
    name: Optional[str] = None
    owner_name: Optional[str] = None
    link: Optional[object] = None
    query_ids: Optional[List[int]] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxPreset":
        from ..CxLink import CxLink

        return cls(
            id=item.get("id"),
            name=item.get("name"),
            owner_name=item.get("ownerName"),
            link=CxLink.from_dict(item.get("link") or {}),
            query_ids=item.get("queryIds"),
        )
