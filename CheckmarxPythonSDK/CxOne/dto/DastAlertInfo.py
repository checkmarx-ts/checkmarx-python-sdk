from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastAlertInfo:
    """Response from .../alert/{alert_id}/info (both the plain and
    manual-findings variants)."""
    name: Optional[str] = None
    severity: Optional[str] = None
    state: Optional[str] = None
    state_id: Optional[int] = None
    description: Optional[str] = None
    solution: Optional[str] = None
    compliance: List[str] = field(default_factory=list)
    status: Optional[str] = None
    cwe_id: Optional[str] = None
    wasc_id: Optional[str] = None
    notes_data: List[dict] = field(default_factory=list)
    changelog_data: List[dict] = field(default_factory=list)
    correlation_status: Optional[str] = None
    correlation_findings_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertInfo":
        return cls(
            name=item.get("name"),
            severity=item.get("severity"),
            state=item.get("state"),
            state_id=item.get("state_id"),
            description=item.get("description"),
            solution=item.get("solution"),
            compliance=list(item.get("compliance") or []),
            status=item.get("status"),
            cwe_id=item.get("cwe_id"),
            wasc_id=item.get("wasc_id"),
            notes_data=list(item.get("notes_data") or []),
            changelog_data=list(item.get("changelog_data") or []),
            correlation_status=item.get("correlation_status"),
            correlation_findings_count=item.get("correlation_findings_count"),
        )
