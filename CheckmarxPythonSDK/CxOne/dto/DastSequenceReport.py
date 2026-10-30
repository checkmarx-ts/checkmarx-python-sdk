from dataclasses import dataclass, field
from typing import List, Optional

from .DastRecordingReport import DastRecordingReport


@dataclass
class DastSequenceReport:
    """An entry in `sequences[]` on DastSequencesReport."""
    name: Optional[str] = None
    position: Optional[int] = None
    recordings: List[DastRecordingReport] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequenceReport":
        return cls(
            name=item.get("name"),
            position=item.get("position"),
            recordings=[
                DastRecordingReport.from_dict(r)
                for r in (item.get("recordings") or [])
            ],
        )
