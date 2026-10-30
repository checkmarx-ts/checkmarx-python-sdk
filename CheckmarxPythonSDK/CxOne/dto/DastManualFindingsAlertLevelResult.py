from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastManualFindingsAlertLevelResult:
    """An entry in `results[]` on GET .../manual_findings/alert_level."""
    id: Optional[str] = None
    state: Optional[str] = None
    severity: Optional[str] = None
    name: Optional[str] = None
    num_instances: Optional[int] = None
    status: Optional[str] = None
    compliance: List[str] = field(default_factory=list)
    cwe_id: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastManualFindingsAlertLevelResult":
        return cls(
            id=item.get("id"),
            state=item.get("state"),
            severity=item.get("severity"),
            name=item.get("name"),
            num_instances=item.get("num_instances"),
            status=item.get("status"),
            compliance=list(item.get("compliance") or []),
            cwe_id=item.get("cwe_id"),
            created_at=item.get("created_at"),
        )
