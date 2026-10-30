from dataclasses import dataclass, field
from typing import Dict, Optional

from .AiCoordinatorAutoRemediationConfigPayload import AiCoordinatorAutoRemediationConfigPayload


@dataclass
class AiCoordinatorAutoRemediationAccountConfigItem:
    """One entry in AccountConfigResponse.configurations, for
    feature=auto_remediation."""
    feature: str = "auto_remediation"
    enabled: Optional[bool] = None
    allow_override: Dict[str, bool] = field(default_factory=dict)
    config: Optional[AiCoordinatorAutoRemediationConfigPayload] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAutoRemediationAccountConfigItem":
        config = item.get("config")
        return cls(
            feature=item.get("feature", "auto_remediation"),
            enabled=item.get("enabled"),
            allow_override=dict(item.get("allowOverride") or {}),
            config=(
                AiCoordinatorAutoRemediationConfigPayload.from_dict(config)
                if config else None
            ),
        )
