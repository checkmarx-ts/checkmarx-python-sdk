from dataclasses import dataclass
from typing import List


@dataclass
class DastResultsGroupCount:
    """One bucket from GET /api/dast/mfe-results/results/{scan_id}/group.

    Note this endpoint uses `count` and `group` (singular) — distinct
    from DastEnvironmentGroupCount and DastScanGroupCount which both
    use `item_count` and `groups` (plural).
    """
    count: int = None
    group: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResultsGroupCount":
        return cls(
            count=item.get("count"),
            group=item.get("group"),
        )
