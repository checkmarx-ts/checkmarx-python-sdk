from dataclasses import dataclass, field
from typing import List, Optional

from .DastApplicationEnvironmentInfo import DastApplicationEnvironmentInfo


@dataclass
class DastEnvironmentSummariesCollection:
    """Response from GET /environmentSummaries.

    Reuses DastApplicationEnvironmentInfo -- same ApplicationEnvironmentsResponse
    schema as GET /associatedEnvs/{appId}.
    """
    environments: List[DastApplicationEnvironmentInfo] = field(default_factory=list)
    total_items: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironmentSummariesCollection":
        return cls(
            environments=[
                DastApplicationEnvironmentInfo.from_dict(e)
                for e in (item.get("environments") or [])
            ],
            total_items=item.get("totalItems"),
        )
