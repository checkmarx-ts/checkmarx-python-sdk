from dataclasses import dataclass
from typing import Optional


@dataclass
class DastAverageScansDataResponse:
    """Response from GET /overview/averageScansData/{envId}."""
    average_scanned_paths: Optional[float] = None
    average_scan_duration: Optional[float] = None
    total_scans: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAverageScansDataResponse":
        return cls(
            average_scanned_paths=item.get("averageScannedPaths"),
            average_scan_duration=item.get("averageScanDuration"),
            total_scans=item.get("totalScans"),
        )
