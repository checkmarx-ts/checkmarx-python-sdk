from __future__ import annotations
from typing import List
from dataclasses import dataclass


@dataclass
class ResultsSummaryTree:
    is_leaf: bool = None
    title: str = None
    key: str = None
    children: List[ResultsSummaryTree] = None
    data: dict = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResultsSummaryTree":
        return cls(
            is_leaf=item.get("isLeaf"),
            title=item.get("title"),
            key=item.get("key"),
            children=[cls.from_dict(child) for child in (item.get("children") or [])],
            data=item.get("data"),
        )
