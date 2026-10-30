from dataclasses import dataclass
from typing import Optional

from .AiCoordinatorAutoRemediationProjectConfigPayload import AiCoordinatorAutoRemediationProjectConfigPayload


@dataclass
class AiCoordinatorAutoRemediationProjectConfigWriteItem:
    """One entry in the `configurations` array of a PUT
    /projects/{project_id}/configuration request body, for
    feature=auto_remediation.

    No `allowOverride` field here -- a project can't grant itself
    override permissions; that's account-only.
    """
    enabled: Optional[bool] = None
    config: Optional[AiCoordinatorAutoRemediationProjectConfigPayload] = None
    feature: str = "auto_remediation"

    def to_dict(self) -> dict:
        raw = {
            "feature": self.feature,
            "enabled": self.enabled,
            "config": self.config.to_dict() if self.config else None,
        }
        return {k: v for k, v in raw.items() if v is not None}
