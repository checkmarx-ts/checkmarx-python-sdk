from dataclasses import dataclass
from typing import List
from .DastScan import DastScan


@dataclass
class DastScansCollection:
    """Top-level response of GET /api/dast/scans/scans.

    The doc names the count field `totalCount`, but the live API
    returns `totalScans`. The DTO reads `totalScans` first and falls
    back to `totalCount` so we're covered either way.
    """
    scans: List[DastScan] = None
    total_scans: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScansCollection":
        return cls(
            scans=[DastScan.from_dict(s) for s in (item.get("scans") or [])],
            total_scans=item.get("totalScans", item.get("totalCount")),
        )
