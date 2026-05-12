from dataclasses import dataclass
from typing import List
from .ResultResponse import ResultResponse


@dataclass
class ResultsResponse:
    data: List[ResultResponse] = None
    total_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResultsResponse":
        return cls(
            data=[ResultResponse.from_dict(r) for r in (item.get("data") or [])],
            total_count=item.get("totalCount"),
        )
