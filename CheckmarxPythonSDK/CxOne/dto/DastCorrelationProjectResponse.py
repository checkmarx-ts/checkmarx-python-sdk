from dataclasses import dataclass
from typing import Optional


@dataclass
class DastCorrelationProjectResponse:
    """An entry in `projects[]` on CorrelationScanResponse."""
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    source_id: Optional[str] = None
    scan_id: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCorrelationProjectResponse":
        return cls(
            project_id=item.get("projectId"),
            project_name=item.get("projectName"),
            source_id=item.get("sourceId"),
            scan_id=item.get("scanId"),
        )
