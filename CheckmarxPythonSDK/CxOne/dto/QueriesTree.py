from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class QueriesTree:
    is_leaf: bool = None
    title: str = None
    key: str = None
    children: List[QueriesTree] = None


def construct_queries_tree(item):
    return QueriesTree(
        is_leaf=item.get("isLeaf"),
        title=item.get("title"),
        key=item.get("key"),
        children=[
            construct_queries_tree(child) for child in item.get("children", [])
        ]
    )
