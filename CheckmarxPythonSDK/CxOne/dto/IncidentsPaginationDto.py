from dataclasses import dataclass, field
from typing import List, Optional

from .IncidentWebDto import IncidentWebDto


@dataclass
class IncidentsPaginationDto:
    """Paginated response from the GET /incidents* endpoints (non-enhanced).

    Attributes:
        incidents (List[IncidentWebDto]): Incidents on the current page.
        filteredIncidentsCount (Optional[int]): Total count after filtering.
    """

    incidents: List[IncidentWebDto] = field(default_factory=list)
    filteredIncidentsCount: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "IncidentsPaginationDto":
        return cls(
            incidents=[
                IncidentWebDto.from_dict(i) for i in (item.get("incidents") or [])
            ],
            filteredIncidentsCount=item.get("filteredIncidentsCount"),
        )
