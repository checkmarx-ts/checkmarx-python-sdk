from dataclasses import dataclass
from typing import Optional

from .RiskLevel import RiskLevel


@dataclass
class DastTimeSpanRiskSummary:
    """The `SpanSummerizedScanRisk` field on EnvironmentsRiskSummary.

    Attribute names avoid leading digits (invalid in Python) --
    `last_30_days`/`from_30_to_60_days`/etc. map to the wire keys
    "last30Days"/"30To60Days"/"60To90Days"/"90Plus".
    """
    last_30_days: Optional[RiskLevel] = None
    from_30_to_60_days: Optional[RiskLevel] = None
    from_60_to_90_days: Optional[RiskLevel] = None
    over_90_days: Optional[RiskLevel] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastTimeSpanRiskSummary":
        return cls(
            last_30_days=(
                RiskLevel.from_dict(item["last30Days"]) if item.get("last30Days") else None
            ),
            from_30_to_60_days=(
                RiskLevel.from_dict(item["30To60Days"]) if item.get("30To60Days") else None
            ),
            from_60_to_90_days=(
                RiskLevel.from_dict(item["60To90Days"]) if item.get("60To90Days") else None
            ),
            over_90_days=(
                RiskLevel.from_dict(item["90Plus"]) if item.get("90Plus") else None
            ),
        )
