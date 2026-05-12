from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CxScanFailedQueries:

    id: Optional[int] = None
    failed_queries: Optional[List] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanFailedQueries":
        return cls(
            id=item.get("id"),
            failed_queries=item.get("failedQueries"),
        )
