from dataclasses import dataclass
from typing import Optional


@dataclass
class DastFlagEnabled:
    """Response from GET /correlations/enabled and GET /pentest/enabled."""
    enabled: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastFlagEnabled":
        return cls(enabled=item.get("enabled"))
