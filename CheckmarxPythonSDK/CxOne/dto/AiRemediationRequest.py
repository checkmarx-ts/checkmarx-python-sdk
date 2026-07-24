from dataclasses import dataclass, field
from typing import List

from .RemediationBucket import RemediationBucket


@dataclass
class AiRemediationRequest:
    """Request body for POST /api/remediation/remediate.

    Attributes:
        scanID (str): Scan identifier.
        buckets (List[RemediationBucket]): One or more scanner-specific result
            groups to remediate. Minimum 1 item required.
    """

    scanID: str
    buckets: List[RemediationBucket] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "scanID": self.scanID,
            "buckets": [b.to_dict() for b in self.buckets],
        }
