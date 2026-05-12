from dataclasses import dataclass, field
from typing import List, Optional
from .CxScanResultNode import CxScanResultNode
from .CxScanResultAttackVector import CxScanResultAttackVector


@dataclass
class CxScanResultAttackVectorByBFL:

    scan_id: Optional[int] = None
    query_version_code: Optional[int] = None
    best_fix_location_node: Optional[CxScanResultNode] = None
    attack_vectors: List[CxScanResultAttackVector] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanResultAttackVectorByBFL":
        bfl_node = item.get("bestFixLocationNode")
        return cls(
            scan_id=item.get("scanId"),
            query_version_code=item.get("queryVersion"),
            best_fix_location_node=(
                CxScanResultNode.from_dict(bfl_node) if bfl_node else None
            ),
            attack_vectors=[
                CxScanResultAttackVector.from_dict(av)
                for av in (item.get("attackVectors") or [])
            ],
        )
