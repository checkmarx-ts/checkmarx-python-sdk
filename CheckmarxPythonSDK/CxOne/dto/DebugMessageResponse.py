from dataclasses import dataclass
from typing import List
from .DebugMessage import DebugMessage


@dataclass
class DebugMessageResponse:
    data: List[DebugMessage] = None
    total_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DebugMessageResponse":
        return cls(
            data=item.get("data"),
            total_count=item.get("totalCount"),
        )
