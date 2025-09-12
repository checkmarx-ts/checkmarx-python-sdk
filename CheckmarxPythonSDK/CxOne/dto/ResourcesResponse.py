from dataclasses import dataclass
from typing import List


@dataclass
class ResourcesResponse:
    all: bool = None
    resources: List[dict] = None


def construct_resources_response(item):
    return ResourcesResponse(
        all=item.get("all"),
        resources=[
            {
                "resourceId": resource.get("resourceId"),
                "resourceType": resource.get("resourceType")
            } for resource in item.get("resources")
        ]
    )
