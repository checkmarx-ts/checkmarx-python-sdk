from dataclasses import dataclass, field
from typing import Dict, Optional

from .AiCoordinatorAutoTriageConfigPayload import AiCoordinatorAutoTriageConfigPayload


@dataclass
class AiCoordinatorAutoTriageAccountConfigItem:
    """One entry in AccountConfigResponse.configurations, for
    feature=auto_triage."""
    feature: str = "auto_triage"
    enabled: Optional[bool] = None
    allow_override: Dict[str, bool] = field(default_factory=dict)
    config: Optional[AiCoordinatorAutoTriageConfigPayload] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAutoTriageAccountConfigItem":
        config = item.get("config")
        return cls(
            feature=item.get("feature", "auto_triage"),
            enabled=item.get("enabled"),
            allow_override=dict(item.get("allowOverride") or {}),
            config=(
                AiCoordinatorAutoTriageConfigPayload.from_dict(config)
                if config else None
            ),
        )
