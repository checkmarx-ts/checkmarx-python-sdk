from dataclasses import dataclass
from typing import Optional

from .DastComplianceData import DastComplianceData
from .RiskLevel import RiskLevel


@dataclass
class DastScansOverTime:
    """An entry in `scansOverTime[]` on GET /environment/{envId}/scans-over-time."""
    risk: Optional[RiskLevel] = None
    compliance: Optional[DastComplianceData] = None
    status_data: Optional[dict] = None
    scan_date: Optional[str] = None
    scan_id: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScansOverTime":
        return cls(
            risk=RiskLevel.from_dict(item["risk"]) if item.get("risk") else None,
            compliance=(
                DastComplianceData.from_dict(item["compliance"])
                if item.get("compliance") else None
            ),
            status_data=item.get("statusData"),
            scan_date=item.get("scanDate"),
            scan_id=item.get("scanId"),
        )
