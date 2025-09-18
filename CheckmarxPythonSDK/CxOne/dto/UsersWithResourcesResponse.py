from dataclasses import dataclass
from typing import List
from .UserWithResource import UserWithResource, construct_user_with_resource


@dataclass
class UsersWithResourcesResponse:
    total_count: None = None
    filtered_count: None = None
    users: List[UserWithResource] = None


def construct_users_with_resources_response(item):
    return UsersWithResourcesResponse(
        total_count=item.get("totalCount"),
        filtered_count=item.get("filteredCount"),
        users=[
            construct_user_with_resource(user) for user in item.get("users", [])
        ]
    )
