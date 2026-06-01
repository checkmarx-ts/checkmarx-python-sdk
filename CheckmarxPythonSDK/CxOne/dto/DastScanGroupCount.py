from dataclasses import dataclass
from typing import List


@dataclass
class DastScanGroupCount:
    """One bucket from GET /api/dast/scans/scans/groups.

    Same shape as DastEnvironmentGroupCount but kept as a separate
    type for semantic clarity (scan grouping vs. environment grouping).
    """
    groups: List[str] = None
    item_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanGroupCount":
        return cls(
            groups=item.get("groups"),
            item_count=item.get("itemCount"),
        )
