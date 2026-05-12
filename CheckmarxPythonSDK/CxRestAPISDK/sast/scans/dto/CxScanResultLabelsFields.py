from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanResultLabelsFields:

    state: Optional[int] = None
    severity: Optional[int] = None
    user_assignment: Optional[str] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanResultLabelsFields":
        return cls(
            state=item.get("state"),
            severity=item.get("severity"),
            user_assignment=item.get("userAssignment"),
            comment=item.get("comment"),
        )
