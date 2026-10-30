from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastRiskLevelOverTimeResponse:
    """Response from GET /overview/risk_level_over_time/{environment_id}.

    `scans` entries are left as raw dicts (scan_id, scan_date,
    critical_count, high_count, medium_count, low_count, info_count,
    total_count) -- anonymous inline schema, not worth a DTO for a
    chart-data payload.
    """
    scans: List[dict] = field(default_factory=list)
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastRiskLevelOverTimeResponse":
        return cls(scans=list(item.get("scans") or []), total=item.get("total"))
