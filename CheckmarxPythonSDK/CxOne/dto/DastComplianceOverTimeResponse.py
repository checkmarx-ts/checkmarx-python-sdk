from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastComplianceOverTimeResponse:
    """Response from GET /overview/compliance_over_time/{environment_id}.

    `scans` entries are left as raw dicts (scan_id, scan_date,
    total_count, compliance_breakdown{owasp_count,cwe_count,wasc_count})
    -- anonymous inline schemas in the spec, not worth a DTO for a
    chart-data payload.
    """
    scans: List[dict] = field(default_factory=list)
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastComplianceOverTimeResponse":
        return cls(scans=list(item.get("scans") or []), total=item.get("total"))
