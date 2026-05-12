from __future__ import annotations
from typing import List
from dataclasses import dataclass


@dataclass
class SourcesTree:
    is_leaf: bool = None
    title: str = None
    key: str = None
    children: List[SourcesTree] = None
