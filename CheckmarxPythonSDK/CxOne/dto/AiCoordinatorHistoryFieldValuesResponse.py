from dataclasses import dataclass, field
from typing import List, Optional

from .AiCoordinatorHistoryListMetaData import AiCoordinatorHistoryListMetaData


@dataclass
class AiCoordinatorHistoryFieldValuesResponse:
    """Response from GET /history/fieldValues."""
    meta_data: Optional[AiCoordinatorHistoryListMetaData] = None
    values: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorHistoryFieldValuesResponse":
        meta_data = item.get("metaData")
        return cls(
            meta_data=(
                AiCoordinatorHistoryListMetaData.from_dict(meta_data)
                if meta_data else None
            ),
            values=list(item.get("values") or []),
        )
