from dataclasses import dataclass, field
from typing import List
from .ScanInfo import ScanInfo


@dataclass
class ScanInfoCollection:
    total_count: int = None
    scans: List[ScanInfo] = field(default_factory=list)
    missing: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ScanInfoCollection":
        return cls(
            total_count=item.get("totalCount"),
            scans=[ScanInfo.from_dict(s) for s in (item.get("scans") or [])],
            missing=item.get("missing") or [],
        )
