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


def construct_results_summary_tree(item):
    return ResultsSummaryTree(
        is_leaf=item.get("isLeaf"),
        title=item.get("title"),
        key=item.get("key"),
        children=[
            construct_results_summary_tree(child) for child in item.get("children", [])
        ],
        data=item.get("data")
    )
