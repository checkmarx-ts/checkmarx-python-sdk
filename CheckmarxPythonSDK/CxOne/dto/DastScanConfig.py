from dataclasses import dataclass
from typing import List
from .DastScanAuth import DastScanAuth
from .DastSessionManagement import DastSessionManagement
from .DastScanUser import DastScanUser


@dataclass
class DastScanConfig:
    """The `scanConfig` object on a DAST environment — the actual config
    used by the scanner. This is the field the live API returns; the
    documented `settings.cliSettings`/`authSettings`/`includePaths`
    shape is not present in practice."""
    authentication: DastScanAuth = None
    include_paths: List[str] = None
    scan_url: str = None
    session_management: DastSessionManagement = None
    users: List[DastScanUser] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanConfig":
        return cls(
            authentication=DastScanAuth.from_dict(item["Authentication"]) if item.get("Authentication") else None,
            include_paths=item.get("IncludePaths"),
            scan_url=item.get("ScanURL"),
            session_management=DastSessionManagement.from_dict(item["SessionManagement"]) if item.get("SessionManagement") else None,
            users=[DastScanUser.from_dict(u) for u in (item.get("Users") or [])],
        )
