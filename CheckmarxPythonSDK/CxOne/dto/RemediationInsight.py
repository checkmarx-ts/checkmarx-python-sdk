from dataclasses import dataclass
from typing import Optional


@dataclass
class RemediationInsight:
    """Remediation summary embedded in a risk from GET /api/risks/ai-insights.

    Attributes:
        status (str): NOT_STARTED, IN_PROGRESS, COMPLETED, or FAILED.
        completedAt (str): RFC3339 datetime when remediation completed.
    """

    status: Optional[str] = None
    completedAt: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RemediationInsight":
        return cls(
            status=item.get("status"),
            completedAt=item.get("completedAt"),
        )
