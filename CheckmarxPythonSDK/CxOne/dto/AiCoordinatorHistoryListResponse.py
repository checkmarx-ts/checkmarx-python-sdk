from dataclasses import dataclass, field
from typing import List, Optional

from .AiCoordinatorHistoryListMetaData import AiCoordinatorHistoryListMetaData
from .AiCoordinatorHistoryItem import AiCoordinatorHistoryItem


@dataclass
class AiCoordinatorHistoryListResponse:
    """Response from GET /history."""
    meta_data: Optional[AiCoordinatorHistoryListMetaData] = None
    history: List[AiCoordinatorHistoryItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorHistoryListResponse":
        meta_data = item.get("metaData")
        return cls(
            meta_data=(
                AiCoordinatorHistoryListMetaData.from_dict(meta_data)
                if meta_data else None
            ),
            history=[
                AiCoordinatorHistoryItem.from_dict(h)
                for h in (item.get("history") or [])
            ],
        )
