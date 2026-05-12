from dataclasses import dataclass, field
from typing import List, Optional
from .CxScanResultNode import CxScanResultNode


@dataclass
class CxScanResultAttackVector:

    result_id: Optional[str] = None
    best_fix_location_node: Optional[int] = None
    nodes: List[CxScanResultNode] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanResultAttackVector":
        return cls(
            result_id=item.get("resultId"),
            best_fix_location_node=item.get("bestFixLocationNode"),
            nodes=[CxScanResultNode.from_dict(n) for n in (item.get("nodes") or [])],
        )
