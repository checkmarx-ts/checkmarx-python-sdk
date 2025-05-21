from __future__ import annotations
from typing import List


class SourcesTree(object):
    def __init__(self, is_leaf: bool = None, title: str = None, key: str = None, children: List[SourcesTree] = None):
        self.isLeaf = is_leaf
        self.title = title
        self.key = key
        self.children = children

    def __str__(self):
        return f"SourcesTree(isLeaf={self.isLeaf}, title={self.title}, key={self.key}, children={self.children})"
