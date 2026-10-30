from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class DastScansCountBySource:
    """An entry in `countBySource[]` on GET /overview/scansCount/{envId}."""
    source: Optional[str] = None
    counts: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item: dict) -> "DastScansCountBySource":
        return cls(
            source=item.get("source"),
            counts=dict(item.get("counts") or {}),
        )
