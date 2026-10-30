from dataclasses import dataclass
from typing import Optional


@dataclass
class DastAuthSessionSummaryItem:
    """An entry in `summary[]` on GET /authSession/{envId}/reportData."""
    key: Optional[str] = None
    description: Optional[str] = None
    passed: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSessionSummaryItem":
        return cls(
            key=item.get("key"),
            description=item.get("description"),
            passed=item.get("passed"),
        )
