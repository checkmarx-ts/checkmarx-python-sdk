from dataclasses import dataclass
from typing import Optional


@dataclass
class DastAuthSessionStatisticItem:
    """An entry in `statistics[]` on GET /authSession/{envId}/reportData."""
    key: Optional[str] = None
    description: Optional[str] = None
    value: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSessionStatisticItem":
        return cls(
            key=item.get("key"),
            description=item.get("description"),
            value=item.get("value"),
        )
