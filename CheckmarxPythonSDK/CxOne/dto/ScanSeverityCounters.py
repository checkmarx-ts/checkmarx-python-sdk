from dataclasses import dataclass
from typing import Optional


@dataclass
class ScanSeverityCounters:
    """SastComparisonStatus.scan_counters / base_scan_counters --
    total results in one scan by severity (GET
    /api/scans-compare/sast/status).
    """
    critical: Optional[int] = None
    high: Optional[int] = None
    medium: Optional[int] = None
    low: Optional[int] = None
    info: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanSeverityCounters":
        if not item:
            return None
        return cls(
            critical=item.get("CRITICAL"),
            high=item.get("HIGH"),
            medium=item.get("MEDIUM"),
            low=item.get("LOW"),
            info=item.get("INFO"),
        )
