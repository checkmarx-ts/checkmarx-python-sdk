from dataclasses import dataclass
from typing import Optional


@dataclass
class RisksMetaData:
    """Pagination metadata from GET /api/risks/.

    Attributes:
        totalResults (int): Total risk count before filters.
        filteredResults (int): Count after filters applied.
        page (int): Current page number.
        pageSize (int): Number of items per page.
    """

    totalResults: Optional[int] = None
    filteredResults: Optional[int] = None
    page: Optional[int] = None
    pageSize: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RisksMetaData":
        return cls(
            totalResults=item.get("totalResults"),
            filteredResults=item.get("filteredResults"),
            page=item.get("page"),
            pageSize=item.get("pageSize"),
        )
