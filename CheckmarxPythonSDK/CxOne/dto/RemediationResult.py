from dataclasses import dataclass
from typing import Optional

from .AutoPr import AutoPr
from .RemediationData import RemediationData


@dataclass
class RemediationResult:
    """Remediation details for a single vulnerability result."""

    resultID: str = None
    createdAt: str = None
    finishedAt: str = None
    autoPr: Optional[AutoPr] = None
    data: Optional[RemediationData] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RemediationResult":
        return cls(
            resultID=item.get("resultID"),
            createdAt=item.get("createdAt"),
            finishedAt=item.get("finishedAt"),
            autoPr=AutoPr.from_dict(item["autoPr"]) if item.get("autoPr") else None,
            data=RemediationData.from_dict(item["data"]) if item.get("data") else None,
        )
