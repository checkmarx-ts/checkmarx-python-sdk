from dataclasses import dataclass, field
from typing import List, Optional

from .EnhancedIncidentsWebDTO import EnhancedIncidentsWebDTO


@dataclass
class EnhancedIncidentsPaginationDTO:
    """Paginated response from GET /incidents/filters/v2.

    Attributes:
        incidents (List[EnhancedIncidentsWebDTO]): Incidents on the current page.
        filteredIncidentsCount (Optional[int]): Total count after filtering.
    """

    incidents: List[EnhancedIncidentsWebDTO] = field(default_factory=list)
    filteredIncidentsCount: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "EnhancedIncidentsPaginationDTO":
        return cls(
            incidents=[
                EnhancedIncidentsWebDTO.from_dict(i)
                for i in (item.get("incidents") or [])
            ],
            filteredIncidentsCount=item.get("filteredIncidentsCount"),
        )
