from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastGroups:
    """An entry in the grouped-results response of GET .../alert_level/group,
    GET .../group, and the manual-findings equivalents."""
    count: Optional[int] = None
    group: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastGroups":
        return cls(count=item.get("count"), group=list(item.get("group") or []))
