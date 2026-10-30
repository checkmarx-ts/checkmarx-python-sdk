from dataclasses import dataclass
from typing import Optional


@dataclass
class AiCoordinatorHistoryListMetaData:
    """Pagination envelope matching platform list style, shared by
    GET /history and GET /history/fieldValues."""
    total_results: Optional[int] = None
    filtered_results: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorHistoryListMetaData":
        return cls(
            total_results=item.get("totalResults"),
            filtered_results=item.get("filteredResults"),
            page=item.get("page"),
            page_size=item.get("pageSize"),
        )
