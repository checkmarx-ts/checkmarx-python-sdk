from dataclasses import dataclass
from typing import Optional


@dataclass
class AiRemediationResponse:
    """Response from POST /api/remediation/remediate (202 Accepted).

    Attributes:
        status (str): Always 'accepted' when the request is successfully
            accepted for processing.
        published (bool): True if a new remediation job was submitted; False if
            an identical request already exists and no duplicate was created.
        existingState (str or None): Current state of the existing remediation
            job when published is False; otherwise None.
        remediationJobId (str): Unique identifier assigned to the remediation
            operation.
    """

    status: str = "accepted"
    published: bool = True
    existingState: Optional[str] = None
    remediationJobId: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiRemediationResponse":
        return cls(
            status=item.get("status", "accepted"),
            published=item.get("published", True),
            existingState=item.get("existingState"),
            remediationJobId=item.get("remediationJobId"),
        )
