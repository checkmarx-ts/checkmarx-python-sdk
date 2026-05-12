from dataclasses import dataclass
from .ResultNode import ResultNode
from .SastResult import SastResult
from typing import List


@dataclass
class BflTree:
    id: str = None
    bfl: ResultNode = None
    results: List[SastResult] = None
    additional_properties: dict = None

    @classmethod
    def from_dict(cls, item: dict) -> "BflTree":
        return cls(
            id=item.get("id"),
            bfl=ResultNode.from_dict(item.get("bfl")),
            results=[SastResult.from_dict(r) for r in (item.get("results") or [])],
            additional_properties=item.get("additionalProperties"),
        )
