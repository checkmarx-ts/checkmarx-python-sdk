from dataclasses import dataclass, field
from typing import List, Optional

from .ScanSeverityCounters import ScanSeverityCounters
from .SeverityStatusCounter import SeverityStatusCounter


@dataclass
class SastComparisonStatus:
    """Response from GET /api/scans-compare/sast/status."""
    severity_status_counters: List[SeverityStatusCounter] = field(
        default_factory=list
    )
    scan_counters: Optional[ScanSeverityCounters] = None
    base_scan_counters: Optional[ScanSeverityCounters] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SastComparisonStatus":
        if not item:
            return None
        return cls(
            severity_status_counters=[
                SeverityStatusCounter.from_dict(s)
                for s in (item.get("severityStatusCounters") or [])
            ],
            scan_counters=ScanSeverityCounters.from_dict(
                item.get("scanCounters")
            ),
            base_scan_counters=ScanSeverityCounters.from_dict(
                item.get("baseScanCounters")
            ),
        )
