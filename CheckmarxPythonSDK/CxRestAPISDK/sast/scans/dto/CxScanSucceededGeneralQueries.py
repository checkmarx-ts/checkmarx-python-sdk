from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanSucceededGeneralQueries:

    scan_id: Optional[int] = None
    general_queries_result_count: Optional[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanSucceededGeneralQueries":
        return cls(
            scan_id=item.get("id"),
            general_queries_result_count=item.get("generalQueriesResultCount"),
        )
