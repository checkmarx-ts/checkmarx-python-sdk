from dataclasses import dataclass
from typing import List, Union
from .RiskLevel import RiskLevel
from .DastAlertRiskLevel import DastAlertRiskLevel
from .DastApplication import DastApplication
from .DastScanConfig import DastScanConfig
from .DastLastRiskRating import DastLastRiskRating
from .DastScanType import DastScanType


def _coerce_risk_rating(value):
    """The doc enumerates High/Medium/Low/None, but the live API has been
    observed to return descriptive strings like 'High risk' / 'No risk'.
    Try the enum first; fall back to the raw string for unknown values."""
    if value is None:
        return None
    try:
        return DastLastRiskRating.get(value)
    except ValueError:
        return value


def _coerce_scan_type(value):
    """Documented enum: DAST | DASTAPI. Fall back to raw string if a future
    value lands before the SDK is updated."""
    if value is None:
        return None
    try:
        return DastScanType.get(value)
    except ValueError:
        return value


@dataclass
class DastEnvironment:
    environment_id: str = None
    tunnel_id: str = None
    domain: str = None
    url: str = None
    scan_type: Union[DastScanType, str] = None
    project_ids: List[str] = None
    tags: List[str] = None
    groups: List[str] = None
    is_public: bool = None
    has_auth: bool = None
    created: str = None
    creator: str = None
    applications: List[DastApplication] = None
    risk_level: RiskLevel = None
    alert_risk_level: DastAlertRiskLevel = None
    risk_rating: Union[DastLastRiskRating, str] = None
    last_alert_risk_rating: str = None
    last_scan_id: str = None
    last_scan_time: str = None
    last_status: str = None
    last_correlation_status: str = None
    auth_success: bool = None
    auth_method: str = None
    last_auth_uuid: str = None
    last_auth_success: bool = None
    has_report: bool = None
    tunnel_state: str = None
    scan_config: DastScanConfig = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironment":
        return cls(
            environment_id=item.get("environmentId"),
            tunnel_id=item.get("tunnelId"),
            domain=item.get("domain"),
            url=item.get("url"),
            scan_type=_coerce_scan_type(item.get("scanType")),
            project_ids=item.get("projectIds"),
            tags=item.get("tags"),
            groups=item.get("groups"),
            is_public=item.get("isPublic"),
            has_auth=item.get("hasAuth"),
            created=item.get("created"),
            creator=item.get("creator"),
            applications=[
                DastApplication.from_dict(a) for a in (item.get("applications") or [])
            ],
            risk_level=RiskLevel.from_dict(item["riskLevel"]) if item.get("riskLevel") else None,
            alert_risk_level=DastAlertRiskLevel.from_dict(item["alertRiskLevel"]) if item.get("alertRiskLevel") else None,
            risk_rating=_coerce_risk_rating(item.get("riskRating")),
            last_alert_risk_rating=item.get("lastAlertRiskRating"),
            last_scan_id=item.get("lastScanID"),
            last_scan_time=item.get("lastScanTime"),
            last_status=item.get("lastStatus"),
            last_correlation_status=item.get("lastCorrelationStatus"),
            auth_success=item.get("authSuccess"),
            auth_method=item.get("authMethod"),
            last_auth_uuid=item.get("lastAuthUUID"),
            last_auth_success=item.get("lastAuthSuccess"),
            has_report=item.get("hasReport"),
            tunnel_state=item.get("tunnelState"),
            scan_config=DastScanConfig.from_dict(item["scanConfig"]) if item.get("scanConfig") else None,
        )
