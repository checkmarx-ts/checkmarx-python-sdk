from dataclasses import dataclass, field
from typing import Dict, Optional

from .AiCoordinatorAutoTriageProjectConfigPayload import AiCoordinatorAutoTriageProjectConfigPayload


@dataclass
class AiCoordinatorAutoTriageProjectConfigItem:
    """One entry in ProjectConfigResponse.configurations, for
    feature=auto_triage."""
    feature: str = "auto_triage"
    enabled: Optional[bool] = None
    config: Optional[AiCoordinatorAutoTriageProjectConfigPayload] = None
    allow_override: Dict[str, bool] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAutoTriageProjectConfigItem":
        config = item.get("config")
        return cls(
            feature=item.get("feature", "auto_triage"),
            enabled=item.get("enabled"),
            config=(
                AiCoordinatorAutoTriageProjectConfigPayload.from_dict(config)
                if config else None
            ),
            allow_override=dict(item.get("allowOverride") or {}),
        )
