from dataclasses import dataclass
from typing import List


@dataclass
class ResourcesResponse:
    all: bool = None
    resources: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResourcesResponse":
        return cls(
            all=item.get("all"),
            resources=[
                {
                    "resourceId": r.get("resourceId"),
                    "resourceType": r.get("resourceType"),
                }
                for r in (item.get("resources") or [])
            ],
        )
