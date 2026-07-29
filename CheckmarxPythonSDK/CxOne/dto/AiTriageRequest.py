from dataclasses import dataclass, field
from typing import List

from .TriageBucket import TriageBucket


@dataclass
class AiTriageRequest:
    """Request body for POST /api/ai-triage/triage.

    Attributes:
        scanID (str): Scan identifier.
        buckets (List[TriageBucket]): Scanner-specific result groups to triage.
    """

    scanID: str
    buckets: List[TriageBucket] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "scanID": self.scanID,
            "buckets": [b.to_dict() for b in self.buckets],
        }
