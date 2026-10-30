from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastAlertInstance:
    """An entry in `instances[]` on GET .../alert/{alert_id}/instances.

    `pentest_findings` is left as a raw list -- PentestFindingLink wasn't
    modeled separately since this is the only place it's nested.
    """
    similarity_id_2: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    correlation_findings_count: Optional[int] = None
    correlation_status: Optional[str] = None
    pentest_findings: List[dict] = field(default_factory=list)
    has_screenshots: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertInstance":
        return cls(
            similarity_id_2=item.get("similarity_id_2"),
            method=item.get("method"),
            path=item.get("path"),
            url=item.get("url"),
            status=item.get("status"),
            source=item.get("source"),
            correlation_findings_count=item.get("correlation_findings_count"),
            correlation_status=item.get("correlation_status"),
            pentest_findings=list(item.get("pentest_findings") or []),
            has_screenshots=item.get("has_screenshots"),
        )
