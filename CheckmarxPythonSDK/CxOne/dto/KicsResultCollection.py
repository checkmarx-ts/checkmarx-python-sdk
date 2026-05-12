from dataclasses import dataclass
from typing import List
from .KicsResult import KicsResult


@dataclass
class KicsResultCollection:
    results: List[KicsResult]
    total_count: int

    @classmethod
    def from_dict(cls, item: dict) -> "KicsResultCollection":
        return cls(
            results=[KicsResult.from_dict(r) for r in (item.get("results") or [])],
            total_count=item.get("totalCount"),
        )
