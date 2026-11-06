from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ScaExportFileFormats:
    """An entry in the response array of GET /api/sca/export/file-formats
    -- the fileFormat values accepted by one export route.
    """
    route: Optional[str] = None  # e.g. "/requests", "/queries"
    file_formats: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ScaExportFileFormats":
        return cls(
            route=item.get("route"),
            file_formats=list(item.get("fileFormats") or []),
        )
