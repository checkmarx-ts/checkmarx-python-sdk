from dataclasses import dataclass
from typing import List
from .Assignment import Assignment


@dataclass
class AssignmentsForResource:
    """
    Attributes:
        resource_id (str): The unique identifier of the resource
        assignments (List[Assignment]):
    """

    resource_id: str = None
    assignments: List[Assignment] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AssignmentsForResource":
        return cls(
            resource_id=item.get("resourceID"),
            assignments=[
                Assignment.from_dict(a) for a in (item.get("assignments") or [])
            ],
        )
