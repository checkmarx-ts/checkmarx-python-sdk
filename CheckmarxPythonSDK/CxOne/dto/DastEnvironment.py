from dataclasses import dataclass
from typing import List
from .RiskLevel import RiskLevel


@dataclass
class DastEnvironment:
    environment_id: str = None
    tunnel_id: str = None
    domain: str = None
    url: str = None
    scan_type: str = None
    project_ids: List[str] = None
    tags: List[str] = None
    groups: List[str] = None
    is_public: bool = None
    has_auth: bool = None
    created: str = None
    settings: dict = None
    applications: List[dict] = None
    risk_level: RiskLevel = None
    alert_risk_level: dict = None
    risk_rating: str = None
    last_alert_risk_rating: str = None
    last_scan_id: str = None
    last_scan_time: str = None
    last_status: str = None
    auth_success: bool = None
    auth_method: str = None
    last_auth_uuid: str = None
    last_auth_success: bool = None
    has_report: bool = None
    tunnel_state: str = None
    scan_config: dict = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironment":
        return cls(
            environment_id=item.get("environmentId"),
            tunnel_id=item.get("tunnelId"),
            domain=item.get("domain"),
            url=item.get("url"),
            scan_type=item.get("scanType"),
            project_ids=item.get("projectIds"),
            tags=item.get("tags"),
            groups=item.get("groups"),
            is_public=item.get("isPublic"),
            has_auth=item.get("hasAuth"),
            created=item.get("created"),
            settings=item.get("settings"),
            applications=item.get("applications"),
            risk_level=RiskLevel.from_dict(item["riskLevel"]) if item.get("riskLevel") else None,
            alert_risk_level=item.get("alertRiskLevel"),
            risk_rating=item.get("riskRating"),
            last_alert_risk_rating=item.get("lastAlertRiskRating"),
            last_scan_id=item.get("lastScanID"),
            last_scan_time=item.get("lastScanTime"),
            last_status=item.get("lastStatus"),
            auth_success=item.get("authSuccess"),
            auth_method=item.get("authMethod"),
            last_auth_uuid=item.get("lastAuthUUID"),
            last_auth_success=item.get("lastAuthSuccess"),
            has_report=item.get("hasReport"),
            tunnel_state=item.get("tunnelState"),
            scan_config=item.get("scanConfig"),
        )
