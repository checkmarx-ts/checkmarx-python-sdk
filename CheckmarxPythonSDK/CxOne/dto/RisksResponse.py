from dataclasses import dataclass, field
from typing import List, Optional

from .Risk import Risk
from .RisksMetaData import RisksMetaData


@dataclass
class RisksResponse:
    """Response from GET /api/risks/.

    Attributes:
        metaData (RisksMetaData): Pagination metadata.
        risks (List[Risk]): List of risks for the project.
    """

    metaData: Optional[RisksMetaData] = None
    risks: List[Risk] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "RisksResponse":
        return cls(
            metaData=(
                RisksMetaData.from_dict(item["metaData"])
                if item.get("metaData")
                else None
            ),
            risks=[
                Risk.from_dict(r) for r in (item.get("risks") or [])
            ],
        )
