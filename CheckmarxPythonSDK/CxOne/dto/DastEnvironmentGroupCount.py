from dataclasses import dataclass
from typing import List


@dataclass
class DastEnvironmentGroupCount:
    """One bucket from GET /api/dast/scans/environments/groups.

    `groups` is a tuple of values corresponding positionally to the
    `groupBy` columns the caller passed (e.g. groupBy=["scantype",
    "domain"] yields groups=["DAST", "example.com"]).
    """
    groups: List[str] = None
    item_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironmentGroupCount":
        return cls(
            groups=item.get("groups"),
            item_count=item.get("itemCount"),
        )
