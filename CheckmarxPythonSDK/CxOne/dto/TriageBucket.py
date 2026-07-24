from dataclasses import dataclass, field
from typing import List


@dataclass
class TriageBucket:
    """A scanner-specific group of result IDs to triage.

    Attributes:
        scannerType (str): The scanner that produced the vulnerabilities.
            Allowed values: 'sast', 'sca' (case-insensitive).
        resultIDs (List[str]): Result IDs to triage for the scanner. Use the
            alternateId returned by GET /api/results. URL-encoding recommended.
    """

    scannerType: str
    resultIDs: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "scannerType": self.scannerType,
            "resultIDs": self.resultIDs,
        }
