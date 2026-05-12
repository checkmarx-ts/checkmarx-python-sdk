from dataclasses import dataclass
from typing import List
from .CloudInsightAccount import CloudInsightAccount


@dataclass
class PaginatedAccountsListResponse:
    data: List[CloudInsightAccount] = None
    total: int = None
    current_page: int = None
    last_page: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "PaginatedAccountsListResponse":
        return cls(
            data=[CloudInsightAccount.from_dict(a) for a in (item.get("data") or [])],
            total=item.get("total"),
            current_page=item.get("currentPage"),
            last_page=item.get("lastPage"),
        )
