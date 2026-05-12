from dataclasses import dataclass, field
from typing import List
from .Scan import Scan


@dataclass
class ScansCollection:
    total_count: int = None
    filtered_total_count: int = None
    scans: List[Scan] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ScansCollection":
        return cls(
            total_count=item.get("totalCount"),
            filtered_total_count=item.get("filteredTotalCount"),
            scans=[Scan.from_dict(s) for s in (item.get("scans") or [])],
        )
