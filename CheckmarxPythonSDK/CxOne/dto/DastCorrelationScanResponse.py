from dataclasses import dataclass, field
from typing import List, Optional

from .DastCorrelationProjectResponse import DastCorrelationProjectResponse
from .DastCorrelationScanSettings import DastCorrelationScanSettings
from .DastSimilarityIds import DastSimilarityIds


@dataclass
class DastCorrelationScanResponse:
    """An entry in `correlationScans[]` on GET /correlations/scans."""
    uuid: Optional[str] = None
    tenant_id: Optional[str] = None
    environment_id: Optional[str] = None
    correlation_scan_date: Optional[str] = None
    scan_id: Optional[str] = None
    scan_date: Optional[str] = None
    status: Optional[str] = None
    projects: List[DastCorrelationProjectResponse] = field(default_factory=list)
    similarity_ids: List[DastSimilarityIds] = field(default_factory=list)
    settings: Optional[DastCorrelationScanSettings] = None
    initiator: Optional[str] = None
    initiator_id: Optional[str] = None
    source: Optional[str] = None
    duration: Optional[int] = None
    found_instances: Optional[int] = None
    total_instances: Optional[int] = None
    incorrect_reports_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCorrelationScanResponse":
        return cls(
            uuid=item.get("uuid"),
            tenant_id=item.get("tenantId"),
            environment_id=item.get("environmentId"),
            correlation_scan_date=item.get("correlationScanDate"),
            scan_id=item.get("scanId"),
            scan_date=item.get("scanDate"),
            status=item.get("status"),
            projects=[
                DastCorrelationProjectResponse.from_dict(p)
                for p in (item.get("projects") or [])
            ],
            similarity_ids=[
                DastSimilarityIds.from_dict(s)
                for s in (item.get("similarityIds") or [])
            ],
            settings=(
                DastCorrelationScanSettings.from_dict(item["settings"])
                if item.get("settings") else None
            ),
            initiator=item.get("initiator"),
            initiator_id=item.get("initiatorId"),
            source=item.get("source"),
            duration=item.get("duration"),
            found_instances=item.get("foundInstances"),
            total_instances=item.get("totalInstances"),
            incorrect_reports_count=item.get("incorrectReportsCount"),
        )
