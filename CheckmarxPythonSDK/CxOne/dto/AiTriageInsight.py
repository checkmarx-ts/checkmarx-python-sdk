from dataclasses import dataclass
from typing import Optional


@dataclass
class AiTriageInsight:
    """AI triage summary embedded in a risk from GET /api/risks/ai-insights.

    Attributes:
        triageStatus (str): VULNERABLE, PROPOSED_NOT_EXPLOITABLE, etc.
        exploitability (str): UNKNOWN, EXPLOITABLE, NOT_EXPLOITABLE,
            UNDETERMINED.
        reachability (str): UNKNOWN, REACHABLE, NOT_REACHABLE, UNDETERMINED.
        fixability (str): UNKNOWN, FIXABLE, NOT_FIXABLE.
        completedAt (str): RFC3339 datetime when triage completed.
    """

    triageStatus: Optional[str] = None
    exploitability: Optional[str] = None
    reachability: Optional[str] = None
    fixability: Optional[str] = None
    completedAt: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiTriageInsight":
        return cls(
            triageStatus=item.get("triageStatus"),
            exploitability=item.get("exploitability"),
            reachability=item.get("reachability"),
            fixability=item.get("fixability"),
            completedAt=item.get("completedAt"),
        )
