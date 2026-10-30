from dataclasses import dataclass
from typing import Optional


@dataclass
class DastStateCount:
    """An entry in `state_counts[]` on GET /states_summary/{app_id}."""
    state: Optional[str] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastStateCount":
        return cls(state=item.get("state"), count=item.get("count"))
