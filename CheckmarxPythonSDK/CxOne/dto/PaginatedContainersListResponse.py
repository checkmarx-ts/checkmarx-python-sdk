from dataclasses import dataclass
from typing import List
from .CloudInsightContainer import CloudInsightContainer


@dataclass
class PaginatedContainersListResponse:
    data: List[CloudInsightContainer] = None
    total: int = None
    current_page: int = None
    last_page: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "PaginatedContainersListResponse":
        return cls(
            data=[CloudInsightContainer.from_dict(c) for c in (item.get("data") or [])],
            total=item.get("total"),
            current_page=item.get("currentPage"),
            last_page=item.get("lastPage"),
        )
