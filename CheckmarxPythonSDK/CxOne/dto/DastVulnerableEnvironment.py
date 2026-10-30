from dataclasses import dataclass
from typing import Optional

from .RiskLevel import RiskLevel


@dataclass
class DastVulnerableEnvironment:
    """An entry in the response of GET /topVulnerableEnvs/{appId}."""
    application_id: Optional[str] = None
    environment_id: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    scan_id: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastVulnerableEnvironment":
        return cls(
            application_id=item.get("ApplicationID"),
            environment_id=item.get("EnvironmentID"),
            domain=item.get("Domain"),
            url=item.get("URL"),
            risk_level=(
                RiskLevel.from_dict(item["RiskLevel"]) if item.get("RiskLevel") else None
            ),
            scan_id=item.get("ScanID"),
        )
