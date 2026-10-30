from dataclasses import dataclass
from typing import Optional


@dataclass
class DastRecordingReport:
    """An entry in `recordings[]` on DastSequenceReport."""
    name: Optional[str] = None
    position: Optional[int] = None
    failed: Optional[bool] = None
    error: Optional[str] = None
    screenshot: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastRecordingReport":
        return cls(
            name=item.get("name"),
            position=item.get("position"),
            failed=item.get("failed"),
            error=item.get("error"),
            screenshot=item.get("screenshot"),
        )
