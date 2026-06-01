from dataclasses import dataclass
from typing import List
from .DastEnvironmentSettings import DastEnvironmentSettings


@dataclass
class DastEnvironmentInput:
    """Request body for POST /api/dast/scans/environment.

    `domain`, `url`, and `scan_type` are required by the API.
    scan_type options: "DAST" (Web) or "DASTAPI" (API).
    """
    domain: str = None
    url: str = None
    scan_type: str = None
    project_ids: List[str] = None
    tags: List[str] = None
    groups: List[str] = None
    is_public: bool = None
    has_auth: bool = None
    settings: DastEnvironmentSettings = None

    def to_dict(self) -> dict:
        raw = {
            "domain": self.domain,
            "url": self.url,
            "scanType": self.scan_type,
            "projectIds": self.project_ids,
            "tags": self.tags,
            "groups": self.groups,
            "isPublic": self.is_public,
            "hasAuth": self.has_auth,
            "settings": self.settings.to_dict() if self.settings else None,
        }
        return {k: v for k, v in raw.items() if v is not None}
