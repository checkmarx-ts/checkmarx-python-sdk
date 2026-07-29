from dataclasses import dataclass, field
from typing import List, Optional

from .RiskWithAiInsights import RiskWithAiInsights
from .RisksMetaData import RisksMetaData


@dataclass
class RisksAiInsightsResponse:
    """Response from GET /api/risks/ai-insights.

    Attributes:
        metaData (RisksMetaData): Pagination metadata.
        risks (List[RiskWithAiInsights]): Risks with AI triage and remediation
            data.
    """

    metaData: Optional[RisksMetaData] = None
    risks: List[RiskWithAiInsights] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "RisksAiInsightsResponse":
        return cls(
            metaData=(
                RisksMetaData.from_dict(item["metaData"])
                if item.get("metaData")
                else None
            ),
            risks=[
                RiskWithAiInsights.from_dict(r) for r in (item.get("risks") or [])
            ],
        )
