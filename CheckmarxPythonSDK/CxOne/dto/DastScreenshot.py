from dataclasses import dataclass
from typing import Optional


@dataclass
class DastScreenshot:
    """A screenshot ({id, content, content_type}) -- the identical shape
    of both VulnerabilityScreenshot (instance screenshots) and
    ManualFindingScreenshot (manual-finding instance screenshots).

    Attributes:
        id (Optional[str]): The screenshot's ID.
        content (Optional[str]): Base64-encoded image content.
        content_type (Optional[str]): e.g. "image/png".
    """
    id: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScreenshot":
        return cls(
            id=item.get("id"),
            content=item.get("content"),
            content_type=item.get("content_type"),
        )
