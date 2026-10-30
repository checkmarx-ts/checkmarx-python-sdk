from dataclasses import dataclass
from typing import Optional


@dataclass
class DastTopFiveRisks:
    """An entry in the response of GET /results/{scan_id}/top_five_risks."""
    name: Optional[str] = None
    critical_count: Optional[int] = None
    high_count: Optional[int] = None
    medium_count: Optional[int] = None
    low_count: Optional[int] = None
    info_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastTopFiveRisks":
        return cls(
            name=item.get("name"),
            critical_count=item.get("criticalCount"),
            high_count=item.get("highCount"),
            medium_count=item.get("mediumCount"),
            low_count=item.get("lowCount"),
            info_count=item.get("infoCount"),
        )
