from dataclasses import dataclass, field
from typing import Dict, Optional

from .AiCoordinatorAutoRemediationProjectConfigPayload import AiCoordinatorAutoRemediationProjectConfigPayload


@dataclass
class AiCoordinatorAutoRemediationProjectConfigItem:
    """One entry in ProjectConfigResponse.configurations, for
    feature=auto_remediation."""
    feature: str = "auto_remediation"
    enabled: Optional[bool] = None
    config: Optional[AiCoordinatorAutoRemediationProjectConfigPayload] = None
    allow_override: Dict[str, bool] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAutoRemediationProjectConfigItem":
        config = item.get("config")
        return cls(
            feature=item.get("feature", "auto_remediation"),
            enabled=item.get("enabled"),
            config=(
                AiCoordinatorAutoRemediationProjectConfigPayload.from_dict(config)
                if config else None
            ),
            allow_override=dict(item.get("allowOverride") or {}),
        )
