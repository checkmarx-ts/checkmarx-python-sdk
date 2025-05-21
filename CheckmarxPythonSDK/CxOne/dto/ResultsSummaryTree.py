from __future__ import annotations
from typing import List


class ResultsSummaryTree(object):
    def __init__(self, is_leaf: bool = None, title: str = None, key: str = None,
                 children: List[ResultsSummaryTree] = None, data: dict = None):
        self.isLeaf = is_leaf
        self.title = title
        self.key = key
        self.children = children
        self.data = data

    def __str__(self):
        return (f"ResultsSummaryTree(isLeaf={self.isLeaf}, title={self.title}, key={self.key}, "
                f"children={self.children}, data={self.data})")
