from dataclasses import dataclass
from typing import List
from .RuleInput import RuleInput


@dataclass
class ApplicationInput:
    name: str
    description: str = None
    criticality: int = 3
    rules: List[RuleInput] = None
    tags: dict = None
