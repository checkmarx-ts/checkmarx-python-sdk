from dataclasses import dataclass, field
from typing import List, Optional

from .DastLeanEnvironment import DastLeanEnvironment


@dataclass
class DastLeanEnvironmentsCollection:
    """Response from GET /leanEnvironments."""
    environments: List[DastLeanEnvironment] = field(default_factory=list)
    total_items: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastLeanEnvironmentsCollection":
        return cls(
            environments=[
                DastLeanEnvironment.from_dict(e) for e in (item.get("environments") or [])
            ],
            total_items=item.get("totalItems"),
        )
