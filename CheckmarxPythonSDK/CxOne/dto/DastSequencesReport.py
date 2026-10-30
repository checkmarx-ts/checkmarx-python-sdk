from dataclasses import dataclass, field
from typing import List

from .DastSequenceReport import DastSequenceReport


@dataclass
class DastSequencesReport:
    """Response from GET /environments/{envId}/scans/{scanId}/sequences-report."""
    sequences: List[DastSequenceReport] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequencesReport":
        return cls(
            sequences=[
                DastSequenceReport.from_dict(s)
                for s in (item.get("sequences") or [])
            ],
        )
