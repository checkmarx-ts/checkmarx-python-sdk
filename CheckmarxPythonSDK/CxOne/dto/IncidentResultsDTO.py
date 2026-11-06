from dataclasses import dataclass, field
from typing import List, Optional

from .IncidentResultWebDTO import IncidentResultWebDTO
from .ViolationDetailsDTO import ViolationDetailsDTO


@dataclass
class IncidentResultsDTO:
    """Response from GET /incidents/{incidentId}/results.

    Attributes:
        violationDetails (Optional[ViolationDetailsDTO]): The violated
            policy/rule details common to all results.
        results (List[IncidentResultWebDTO]): Results on the current page.
        filteredResultsCount (Optional[int]): Total count after filtering.
    """

    violationDetails: Optional[ViolationDetailsDTO] = None
    results: List[IncidentResultWebDTO] = field(default_factory=list)
    filteredResultsCount: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "IncidentResultsDTO":
        return cls(
            violationDetails=(
                ViolationDetailsDTO.from_dict(item["violationDetails"])
                if item.get("violationDetails")
                else None
            ),
            results=[
                IncidentResultWebDTO.from_dict(r)
                for r in (item.get("results") or [])
            ],
            filteredResultsCount=item.get("filteredResultsCount"),
        )
