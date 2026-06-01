from dataclasses import dataclass
from typing import List
from .DastCliSettings import DastCliSettings
from .DastAuthSettings import DastAuthSettings


@dataclass
class DastEnvironmentSettings:
    cli_settings: DastCliSettings = None
    auth_settings: DastAuthSettings = None
    include_paths: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironmentSettings":
        return cls(
            cli_settings=DastCliSettings.from_dict(item["cliSettings"]) if item.get("cliSettings") else None,
            auth_settings=DastAuthSettings.from_dict(item["authSettings"]) if item.get("authSettings") else None,
            include_paths=item.get("includePaths"),
        )
