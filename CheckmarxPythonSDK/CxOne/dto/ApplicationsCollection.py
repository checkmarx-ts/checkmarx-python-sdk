from dataclasses import dataclass
from typing import List
from .Application import Application


@dataclass
class ApplicationsCollection:
    total_count: int = None
    filtered_total_count: int = None
    applications: List[Application] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ApplicationsCollection":
        return cls(
            total_count=item.get("totalCount"),
            filtered_total_count=item.get("filteredTotalCount"),
            applications=[
                Application.from_dict(a) for a in (item.get("applications") or [])
            ],
        )
