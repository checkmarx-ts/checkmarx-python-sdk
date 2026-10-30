from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastManualFindingInstanceResult:
    """An entry in `results[]` on GET .../manual_findings."""
    risk_id: Optional[str] = None
    alert_id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    severity: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    compliance: List[str] = field(default_factory=list)
    description: Optional[str] = None
    solution: Optional[str] = None
    attack: Optional[str] = None
    evidence: Optional[str] = None
    cwe_id: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastManualFindingInstanceResult":
        return cls(
            risk_id=item.get("risk_id"),
            alert_id=item.get("alert_id"),
            name=item.get("name"),
            url=item.get("url"),
            path=item.get("path"),
            method=item.get("method"),
            severity=item.get("severity"),
            state=item.get("state"),
            status=item.get("status"),
            compliance=list(item.get("compliance") or []),
            description=item.get("description"),
            solution=item.get("solution"),
            attack=item.get("attack"),
            evidence=item.get("evidence"),
            cwe_id=item.get("cwe_id"),
            created_at=item.get("created_at"),
        )
