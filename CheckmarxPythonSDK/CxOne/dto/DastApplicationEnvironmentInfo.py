from dataclasses import dataclass
from typing import Optional


@dataclass
class DastApplicationEnvironmentInfo:
    """An entry in the response of GET /associatedEnvs/{appId} -- a DAST
    Environment associated with an Application."""
    environment_id: Optional[str] = None
    url: Optional[str] = None
    domain: Optional[str] = None
    last_scan_id: Optional[str] = None
    last_scan_status: Optional[str] = None
    is_primary: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastApplicationEnvironmentInfo":
        return cls(
            environment_id=item.get("EnvironmentID"),
            url=item.get("URL"),
            domain=item.get("Domain"),
            last_scan_id=item.get("LastScanID"),
            last_scan_status=item.get("LastScanStatus"),
            is_primary=item.get("IsPrimary"),
        )
