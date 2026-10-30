from dataclasses import dataclass
from typing import Optional


@dataclass
class DastComplianceAnalytics:
    """Response from GET /analytics/compliance/{app_id}."""
    pass_count: Optional[int] = None
    fail_count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastComplianceAnalytics":
        # "pass" is a Python keyword, so it can't be the field name.
        return cls(pass_count=item.get("pass"), fail_count=item.get("fail"))
