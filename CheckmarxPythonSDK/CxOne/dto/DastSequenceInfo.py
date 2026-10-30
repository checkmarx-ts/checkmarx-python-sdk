from dataclasses import dataclass
from typing import Optional


@dataclass
class DastSequenceInfo:
    """A sequence reference nested in DastRecordingWithSequences."""
    id: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequenceInfo":
        return cls(id=item.get("id"), name=item.get("name"))
