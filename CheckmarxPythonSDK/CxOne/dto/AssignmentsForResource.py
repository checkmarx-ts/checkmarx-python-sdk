from dataclasses import dataclass
from typing import List
from .Assignment import Assignment, construct_assignment


@dataclass
class AssignmentsForResource:
    """
    Attributes:
        resource_id (str): The unique identifier of the resource
        assignments (List[Assignment]):
    """
    resource_id: str = None
    assignments: List[Assignment] = None


def construct_assignments_for_resource(item) -> AssignmentsForResource:
    return AssignmentsForResource(
        resource_id=item.get("resourceID"),
        assignments=[
            construct_assignment(assignment) for assignment in item.get("assignments", [])
        ]
    )
