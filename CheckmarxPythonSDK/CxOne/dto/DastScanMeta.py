from dataclasses import dataclass
from typing import Optional


@dataclass
class DastScanMeta:
    """An entry in `lastScans[]` on GET /scans/{envId}/{scanId}/meta."""
    scan_id: Optional[str] = None
    created: Optional[str] = None
    statistics: Optional[str] = None
    failed_sequences_count: Optional[int] = None
    sequences_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanMeta":
        return cls(
            scan_id=item.get("scanId"),
            created=item.get("created"),
            statistics=item.get("statistics"),
            failed_sequences_count=item.get("failedSequencesCount"),
            sequences_count=item.get("sequencesCount"),
        )
