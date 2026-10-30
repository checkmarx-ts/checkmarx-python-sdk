from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastAlertLevelResult:
    """An entry in `results[]` on GET .../alert_level.

    `correlation_findings` and `pentest_findings` are left raw --
    CorrelationFindingsSummary/PentestFindingLink weren't modeled
    separately since they're only nested here.
    """
    alert_similarity_id: Optional[str] = None
    state: Optional[str] = None
    severity: Optional[str] = None
    name: Optional[str] = None
    num_instances: Optional[int] = None
    status: Optional[str] = None
    owasp: List[str] = field(default_factory=list)
    num_notes: Optional[int] = None
    systemic: Optional[bool] = None
    source: Optional[str] = None
    correlation_findings: Optional[dict] = None
    pentest_findings: List[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertLevelResult":
        return cls(
            alert_similarity_id=item.get("alert_similarity_id"),
            state=item.get("state"),
            severity=item.get("severity"),
            name=item.get("name"),
            num_instances=item.get("num_instances"),
            status=item.get("status"),
            owasp=list(item.get("owasp") or []),
            num_notes=item.get("num_notes"),
            systemic=item.get("systemic"),
            source=item.get("source"),
            correlation_findings=item.get("correlation_findings"),
            pentest_findings=list(item.get("pentest_findings") or []),
        )
