from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastStatesOverTimeResponse:
    """Response from GET /overview/states_over_time/{environment_id}.

    `scans` entries are left as raw dicts (scan_id, scan_date,
    total_count, state_counts{<state name>: count}) -- anonymous inline
    schema, not worth a DTO for a chart-data payload.
    """
    scans: List[dict] = field(default_factory=list)
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastStatesOverTimeResponse":
        return cls(scans=list(item.get("scans") or []), total=item.get("total"))
