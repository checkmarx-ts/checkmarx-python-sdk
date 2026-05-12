from dataclasses import dataclass, field
from typing import List
from .Property import Property


@dataclass
class SastScan:
    scan_id: str = None
    state: str = None
    queue_at: str = None
    allocated_at: str = None
    running_at: str = None
    engine: str = None
    properties: List[Property] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "SastScan":
        return cls(
            scan_id=item.get("id"),
            state=item.get("state"),
            queue_at=item.get("queuedAt"),
            allocated_at=item.get("allocatedAt"),
            running_at=item.get("runningAt"),
            engine=item.get("engine"),
            properties=[Property.from_dict(p) for p in (item.get("properties") or [])],
        )
