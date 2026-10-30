from dataclasses import dataclass
from typing import Optional

from .AiCoordinatorAutoTriageConfigPayload import AiCoordinatorAutoTriageConfigPayload
from .AiCoordinatorAutoTriageAllowOverridePayload import AiCoordinatorAutoTriageAllowOverridePayload


@dataclass
class AiCoordinatorAutoTriageAccountConfigWriteItem:
    """One entry in the `configurations` array of a PUT /configuration
    (account) request body, for feature=auto_triage.

    `enabled` is required by the API.
    """
    enabled: Optional[bool] = None
    allow_override: Optional[AiCoordinatorAutoTriageAllowOverridePayload] = None
    config: Optional[AiCoordinatorAutoTriageConfigPayload] = None
    feature: str = "auto_triage"

    def to_dict(self) -> dict:
        raw = {
            "feature": self.feature,
            "enabled": self.enabled,
            "allowOverride": (
                self.allow_override.to_dict() if self.allow_override else None
            ),
            "config": self.config.to_dict() if self.config else None,
        }
        return {k: v for k, v in raw.items() if v is not None}
