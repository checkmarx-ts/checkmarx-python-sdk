from dataclasses import dataclass
from typing import List
from .DastCliSettings import DastCliSettings
from .DastAuthSettings import DastAuthSettings
from .DastConfigFileSettings import DastConfigFileSettings
from .DastCustomHeader import DastCustomHeader
from .DastSessionManagementHeader import DastSessionManagementHeader
from .DastScanOptions import DastScanOptions
from .DastAutomationScript import DastAutomationScript


@dataclass
class DastEnvironmentSettings:
    """Request-side `settings` block. Used by POST and PUT
    /api/dast/scans/environment. The response side uses a different
    `scanConfig` shape — see DastScanConfig.

    `automation_scripts` is documented on PUT only, but the SDK exposes
    it on this shared DTO since the wire path is the same.
    """
    cli_settings: DastCliSettings = None
    auth_settings: DastAuthSettings = None
    config_file_settings: DastConfigFileSettings = None
    custom_headers: List[DastCustomHeader] = None
    session_management: List[DastSessionManagementHeader] = None
    scan_options: DastScanOptions = None
    automation_scripts: List[DastAutomationScript] = None

    def to_dict(self) -> dict:
        raw = {
            "cliSettings": self.cli_settings.to_dict() if self.cli_settings else None,
            "authSettings": self.auth_settings.to_dict() if self.auth_settings else None,
            "configFileSettings": self.config_file_settings.to_dict() if self.config_file_settings else None,
            "customHeaders": [h.to_dict() for h in self.custom_headers] if self.custom_headers else None,
            "sessionManagement": [h.to_dict() for h in self.session_management] if self.session_management else None,
            "scanOptions": self.scan_options.to_dict() if self.scan_options else None,
            "automationScripts": (
                [s.to_dict() for s in self.automation_scripts]
                if self.automation_scripts else None
            ),
        }
        return {k: v for k, v in raw.items() if v is not None}
