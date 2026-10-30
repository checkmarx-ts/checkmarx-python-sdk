from dataclasses import dataclass, field
from typing import List, Optional

from .DastScanMeta import DastScanMeta


@dataclass
class DastScansList:
    """Response from GET /scans/{envId}/{scanId}/meta."""
    last_scans: List[DastScanMeta] = field(default_factory=list)
    current_scan_date: Optional[str] = None
    current_has_sites_tree: Optional[bool] = None
    current_scan_statistics: Optional[str] = None
    current_failed_sequences_count: Optional[int] = None
    current_sequences_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScansList":
        return cls(
            last_scans=[
                DastScanMeta.from_dict(s) for s in (item.get("lastScans") or [])
            ],
            current_scan_date=item.get("currentScanDate"),
            current_has_sites_tree=item.get("currentHasSitesTree"),
            current_scan_statistics=item.get("currentScanStatistics"),
            current_failed_sequences_count=item.get("currentFailedSequencesCount"),
            current_sequences_count=item.get("currentSequencesCount"),
        )
