from dataclasses import dataclass, field
from typing import List, Optional

from .DastCorrelationScanResponse import DastCorrelationScanResponse


@dataclass
class DastCorrelationScansCollection:
    """Response from GET /correlations/scans."""
    correlation_scans: List[DastCorrelationScanResponse] = field(default_factory=list)
    total_correlation_scans: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCorrelationScansCollection":
        return cls(
            correlation_scans=[
                DastCorrelationScanResponse.from_dict(s)
                for s in (item.get("correlationScans") or [])
            ],
            total_correlation_scans=item.get("totalCorrelationScans"),
        )
