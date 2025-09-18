from dataclasses import dataclass
from typing import List
from .AssignmentsWithBaseRoles import AssignmentsWithBaseRoles, construct_assignments_with_base_roles


@dataclass
class EntitiesForExtendedResponse:
    total_count: int = None
    filtered_total_count: int = None
    assignments: List[AssignmentsWithBaseRoles] = None


def construct_entities_for_extended_response(item):
    return EntitiesForExtendedResponse(
        total_count=item.get("totalCount"),
        filtered_total_count=item.get("filteredTotalCount"),
        assignments=[
            construct_assignments_with_base_roles(assignment) for assignment in item.get("assignments", [])
        ]
    )
