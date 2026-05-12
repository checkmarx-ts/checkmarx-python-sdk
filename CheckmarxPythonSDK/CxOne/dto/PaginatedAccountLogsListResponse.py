from dataclasses import dataclass
from typing import List
from .CloudInsightAccountLog import CloudInsightAccountLog


@dataclass
class PaginatedAccountLogsListResponse:
    data: List[CloudInsightAccountLog] = None
    total: int = None
    current_page: int = None
    last_page: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "PaginatedAccountLogsListResponse":
        return cls(
            data=[
                CloudInsightAccountLog.from_dict(log)
                for log in (item.get("data") or [])
            ],
            total=item.get("total"),
            current_page=item.get("currentPage"),
            last_page=item.get("lastPage"),
        )
