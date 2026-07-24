from dataclasses import dataclass


@dataclass
class ReachabilityAnalysis:
    """Allowed status values: UNSPECIFIED, REACHABLE, NOT_REACHABLE, UNCERTAIN."""

    status: str = "UNSPECIFIED"
    reasoning: str = ""

    @classmethod
    def from_dict(cls, item: dict) -> "ReachabilityAnalysis":
        return cls(
            status=item.get("status", "UNSPECIFIED"),
            reasoning=item.get("reasoning", ""),
        )
