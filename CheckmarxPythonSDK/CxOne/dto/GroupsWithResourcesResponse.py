from dataclasses import dataclass
from typing import List
from .GroupWithResource import construct_group_with_resource


@dataclass
class GroupsWithResourcesResponse:
    total_count: int = None
    filtered_count: int = None
    groups: List[dict] = None


def construct_groups_with_resources_response(item):
    return GroupsWithResourcesResponse(
        total_count=item.get("totalCount"),
        filtered_count=item.get("filteredCount"),
        groups=[
            construct_group_with_resource(group) for group in item.get("groups", [])
        ]
    )
