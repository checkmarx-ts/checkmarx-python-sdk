from dataclasses import dataclass
from typing import List, Union
from .RiskLevel import RiskLevel
from .DastScanType import DastScanType
from .DastScanInsight import DastScanInsight


@dataclass
class DastScan:
    """Single scan record from GET /api/dast/scans/scans.

    Modeled from the live response, which diverges from the published
    doc in several places:
      - top-level field is `lastStatus`, not `status`
      - top-level field is `scanDuration`, not `duration`
      - `statistics` is a string, not a nested object
      - `scannedPathsCount` and `complianceData` are top-level, not
        nested under `statistics`
      - the extra fields alertRiskRating, insights, settings, source
        are returned but not documented
    """
    scan_id: str = None
    environment_id: str = None
    initiator: str = None
    scan_type: Union[DastScanType, str] = None
    last_status: str = None
    risk_rating: str = None
    alert_risk_rating: str = None
    created: str = None
    start_time: str = None
    update_time: str = None
    scan_duration: int = None
    tags: List[str] = None
    groups: List[str] = None
    has_results: bool = None
    risk_level: RiskLevel = None
    alert_risk_level: RiskLevel = None
    project_id: str = None
    statistics: str = None
    compliance_data: dict = None
    has_log: bool = None
    scanned_paths_count: int = None
    settings: dict = None
    source: str = None
    insights: List[DastScanInsight] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScan":
        return cls(
            scan_id=item.get("scanId"),
            environment_id=item.get("environmentId"),
            initiator=item.get("initiator"),
            scan_type=item.get("scanType"),
            last_status=item.get("lastStatus"),
            risk_rating=item.get("riskRating"),
            alert_risk_rating=item.get("alertRiskRating"),
            created=item.get("created"),
            start_time=item.get("startTime"),
            update_time=item.get("updateTime"),
            scan_duration=item.get("scanDuration"),
            tags=item.get("tags"),
            groups=item.get("groups"),
            has_results=item.get("hasResults"),
            risk_level=RiskLevel.from_dict(item["riskLevel"]) if item.get("riskLevel") else None,
            alert_risk_level=RiskLevel.from_dict(item["alertRiskLevel"]) if item.get("alertRiskLevel") else None,
            project_id=item.get("projectId"),
            statistics=item.get("statistics"),
            compliance_data=item.get("complianceData"),
            has_log=item.get("hasLog"),
            scanned_paths_count=item.get("scannedPathsCount"),
            settings=item.get("settings"),
            source=item.get("source"),
            insights=[DastScanInsight.from_dict(i) for i in (item.get("insights") or [])],
        )
