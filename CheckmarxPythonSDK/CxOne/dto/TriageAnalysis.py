from dataclasses import dataclass, field
from typing import List

from .ConfidenceScore import ConfidenceScore
from .ReachabilityAnalysis import ReachabilityAnalysis
from .ExploitabilityAnalysis import ExploitabilityAnalysis


@dataclass
class TriageAnalysis:
    confidence: ConfidenceScore = None
    reachability: ReachabilityAnalysis = None
    exploitability: ExploitabilityAnalysis = None
    usage_locations: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "TriageAnalysis":
        return cls(
            confidence=ConfidenceScore.from_dict(item["confidence"]) if item.get("confidence") else None,
            reachability=ReachabilityAnalysis.from_dict(item["reachability"]) if item.get("reachability") else None,
            exploitability=ExploitabilityAnalysis.from_dict(item["exploitability"]) if item.get("exploitability") else None,
            usage_locations=item.get("usage_locations", []),
        )
