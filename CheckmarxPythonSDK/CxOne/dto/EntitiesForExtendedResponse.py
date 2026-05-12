from dataclasses import dataclass
from typing import List
from .AssignmentsWithBaseRoles import AssignmentsWithBaseRoles


@dataclass
class EntitiesForExtendedResponse:
    total_count: int = None
    filtered_total_count: int = None
    assignments: List[AssignmentsWithBaseRoles] = None

    @classmethod
    def from_dict(cls, item: dict) -> "EntitiesForExtendedResponse":
        return cls(
            total_count=item.get("totalCount"),
            filtered_total_count=item.get("filteredTotalCount"),
            assignments=[
                AssignmentsWithBaseRoles.from_dict(a)
                for a in (item.get("assignments") or [])
            ],
        )
