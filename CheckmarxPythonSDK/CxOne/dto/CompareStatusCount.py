from dataclasses import dataclass
from typing import Optional


@dataclass
class CompareStatusCount:
    """An entry in SeverityStatusCounter.results (GET
    /api/scans-compare/sast/status) -- the count of results at one
    status (NEW/RECURRENT/FIXED) within one severity level.
    """
    status: Optional[str] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CompareStatusCount":
        if not item:
            return None
        return cls(
            status=item.get("status"),
            count=item.get("count"),
        )
