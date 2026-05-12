from dataclasses import dataclass
from typing import List
from .Resource import Resource


@dataclass
class PaginatedResourcesList:
    data: List[Resource] = None
    total: int = None
    current_page: int = None
    last_page: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "PaginatedResourcesList":
        return cls(
            data=[Resource.from_dict(r) for r in (item.get("data") or [])],
            total=item.get("total"),
            current_page=item.get("currentPage"),
            last_page=item.get("lastPage"),
        )
