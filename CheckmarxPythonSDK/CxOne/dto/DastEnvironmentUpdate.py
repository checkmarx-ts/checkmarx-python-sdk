from dataclasses import dataclass
from typing import List, Union
from .DastEnvironmentSettings import DastEnvironmentSettings
from .DastAutomationScript import DastAutomationScript
from .DastScanType import DastScanType


@dataclass
class DastEnvironmentUpdate:
    """Request body for PUT /api/dast/scans/environment.

    `environment_id` is required by the API. Note this Update shape
    has appIds/primaryAppIds/automationScripts/tunnelId that the
    Create shape doesn't, and omits hasAuth that Create has.
    """
    environment_id: str = None
    domain: str = None
    url: str = None
    scan_type: Union[DastScanType, str] = None
    project_ids: List[str] = None
    tags: List[str] = None
    groups: List[str] = None
    is_public: bool = None
    app_ids: List[str] = None
    primary_app_ids: List[str] = None
    settings: DastEnvironmentSettings = None
    automation_scripts: List[DastAutomationScript] = None
    tunnel_id: str = None

    def to_dict(self) -> dict:
        raw = {
            "environmentId": self.environment_id,
            "domain": self.domain,
            "url": self.url,
            "scanType": (
                self.scan_type.value if isinstance(self.scan_type, DastScanType)
                else self.scan_type
            ),
            "projectIds": self.project_ids,
            "tags": self.tags,
            "groups": self.groups,
            "isPublic": self.is_public,
            "appIds": self.app_ids,
            "primaryAppIds": self.primary_app_ids,
            "settings": self.settings.to_dict() if self.settings else None,
            "automationScripts": (
                [s.to_dict() for s in self.automation_scripts]
                if self.automation_scripts else None
            ),
            "tunnelId": self.tunnel_id,
        }
        return {k: v for k, v in raw.items() if v is not None}
