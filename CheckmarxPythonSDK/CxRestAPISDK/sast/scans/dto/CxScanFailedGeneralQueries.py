from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CxScanFailedGeneralQueries:

    scan_id: Optional[int] = None
    failed_general_queries: Optional[List] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanFailedGeneralQueries":
        return cls(
            scan_id=item.get("id"),
            failed_general_queries=item.get("failedGeneralQueries"),
        )
