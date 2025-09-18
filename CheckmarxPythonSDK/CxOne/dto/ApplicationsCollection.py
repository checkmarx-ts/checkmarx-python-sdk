from dataclasses import dataclass
from typing import List
from .Application import Application, construct_application


@dataclass
class ApplicationsCollection:
    total_count: int = None
    filtered_total_count: int = None
    applications: List[Application] = None


def construct_applications_collection(item):
    return ApplicationsCollection(
        total_count=item.get("totalCount"),
        filtered_total_count=item.get("filteredTotalCount"),
        applications=[
            construct_application(application) for application in item.get("applications", [])
        ]
    )
