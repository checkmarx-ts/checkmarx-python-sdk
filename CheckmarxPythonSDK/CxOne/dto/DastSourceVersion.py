from dataclasses import dataclass
from typing import Optional


@dataclass
class DastSourceVersion:
    """A value in the response of GET /latestProjectSources/{envId},
    keyed by project ID."""
    source_id: Optional[str] = None
    uploaded_at: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastSourceVersion":
        return cls(
            source_id=item.get("sourceId"),
            uploaded_at=item.get("uploadedAt"),
        )
