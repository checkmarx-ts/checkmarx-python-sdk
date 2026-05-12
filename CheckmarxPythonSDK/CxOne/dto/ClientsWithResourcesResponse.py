from dataclasses import dataclass
from typing import List
from .ClientWithResource import ClientWithResource


@dataclass
class ClientsWithResourcesResponse:
    total_count: int = None
    filtered_count: int = None
    clients: List[ClientWithResource] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientsWithResourcesResponse":
        return cls(
            total_count=item.get("totalCount"),
            filtered_count=item.get("filteredCount"),
            clients=[
                ClientWithResource.from_dict(c) for c in (item.get("clients") or [])
            ],
        )
