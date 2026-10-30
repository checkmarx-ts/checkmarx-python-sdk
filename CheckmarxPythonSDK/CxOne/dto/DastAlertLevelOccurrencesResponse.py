from dataclasses import dataclass, field
from typing import List


@dataclass
class DastAlertLevelOccurrencesResponse:
    """Response from GET /overview/occurrences_over_time/{environment_id}.

    `points` entries are left as raw dicts (timestamp, new_count,
    recurrent_count) -- anonymous inline schema, not worth a DTO for a
    chart-data payload.
    """
    points: List[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertLevelOccurrencesResponse":
        return cls(points=list(item.get("points") or []))
