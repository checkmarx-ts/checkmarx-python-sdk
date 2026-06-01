from dataclasses import dataclass
from typing import List
from .DastEnvironment import DastEnvironment


@dataclass
class DastEnvironmentsCollection:
    environments: List[DastEnvironment] = None
    total_items: int = None
    misconfigured_count: int = None
    zrok_host: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironmentsCollection":
        return cls(
            environments=[
                DastEnvironment.from_dict(e) for e in (item.get("environments") or [])
            ],
            total_items=item.get("totalItems"),
            misconfigured_count=item.get("misconfiguredCount"),
            zrok_host=item.get("zrokHost"),
        )
