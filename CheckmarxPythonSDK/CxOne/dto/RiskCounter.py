from dataclasses import dataclass
from typing import Optional


@dataclass
class RiskCounter:
    """One aggregated risk counter from GET /api/risks/aggregate.

    Attributes:
        severity (str): CRITICAL, HIGH, MEDIUM, LOW, INFO, or empty string
            when groupBy=engine only.
        engine (str): SAST, IAC, SCA, or empty string when groupBy=severity
            only.
        count (int): Number of risks matching this group.
    """

    severity: Optional[str] = None
    engine: Optional[str] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RiskCounter":
        return cls(
            severity=item.get("severity"),
            engine=item.get("engine"),
            count=item.get("count"),
        )
