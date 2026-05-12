from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class QueriesTree:
    is_leaf: bool = None
    title: str = None
    key: str = None
    children: List[QueriesTree] = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueriesTree":
        return cls(
            is_leaf=item.get("isLeaf"),
            title=item.get("title"),
            key=item.get("key"),
            children=[cls.from_dict(child) for child in (item.get("children") or [])],
        )
