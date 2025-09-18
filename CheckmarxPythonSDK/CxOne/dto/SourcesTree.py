from __future__ import annotations
from typing import List
from dataclasses import dataclass


@dataclass
class SourcesTree:
    is_leaf: bool = None
    title: str = None
    key: str = None
    children: List[SourcesTree] = None


def construct_sources_tree(item):
    return SourcesTree(
        is_leaf=item.get("isLeaf"),
        title=item.get("title"),
        key=item.get("Key"),
        children=[
            construct_sources_tree(child) for child in item.get("children", [])
        ]
    )
