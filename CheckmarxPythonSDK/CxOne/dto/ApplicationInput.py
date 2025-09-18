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

    def to_dict(self):
        data = {
            "name": self.name
        }
        if self.description:
            data.update({"description": self.description})
        if self.criticality:
            data.update({"criticality": self.criticality})
        if self.rules:
            data.update({"rules": [
                {
                    "type": rule.type,
                    "value": rule.value,
                } for rule in self.rules
            ]
            })
        if self.tags:
            data.update({"tags": self.tags})
        return data
