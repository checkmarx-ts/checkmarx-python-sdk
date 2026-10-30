from dataclasses import dataclass
from typing import Optional

from .RiskLevel import RiskLevel


@dataclass
class DastEnvironmentsRiskRatingSummary:
    """Response from GET /envsRiskRatingSummary/{appId}."""
    total_environments: Optional[int] = None
    risk_rating_summary: Optional[RiskLevel] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironmentsRiskRatingSummary":
        return cls(
            total_environments=item.get("TotalEnvironments"),
            risk_rating_summary=(
                RiskLevel.from_dict(item["RiskRatingSummary"])
                if item.get("RiskRatingSummary") else None
            ),
        )
