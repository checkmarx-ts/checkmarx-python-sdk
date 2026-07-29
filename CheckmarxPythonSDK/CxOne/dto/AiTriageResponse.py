from dataclasses import dataclass
from typing import Optional


@dataclass
class AiTriageResponse:
    """Response from POST /api/ai-triage/triage (202 Accepted).

    Attributes:
        scanID (str): Scan identifier.
        status (str): Always 'accepted' when the request is successfully
            accepted for processing.
        triageID (str): Unique identifier assigned to the triage operation.
        published (bool): True if a new triage job was submitted; False if an
            identical request already exists and no duplicate was created.
        existingTriageState (str or None): Current state of the existing triage
            job when published is False; otherwise None.
    """

    scanID: str = None
    status: str = None
    triageID: str = None
    published: bool = True
    existingTriageState: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiTriageResponse":
        return cls(
            scanID=item.get("scanID"),
            status=item.get("status"),
            triageID=item.get("triageID"),
            published=item.get("published", True),
            existingTriageState=item.get("existingTriageState"),
        )
