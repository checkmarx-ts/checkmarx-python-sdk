from dataclasses import dataclass
from typing import List
from .GroupRepresentation import GroupRepresentation, construct_group_representation


@dataclass
class GroupsResponse:
    total: int = None
    groups: List[GroupRepresentation] = None


def construct_groups_response(item):
    return GroupsResponse(
        total=item.get("total"),
        groups=[
            construct_group_representation(group) for group in item.get("groups", [])
        ]
    )
