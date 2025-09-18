from dataclasses import dataclass
from typing import List
from .CloudInsightContainer import CloudInsightContainer, construct_cloud_insight_container


@dataclass
class PaginatedContainersListResponse:
    data: List[CloudInsightContainer] = None
    total: int = None
    current_page: int = None
    last_page: int = None


def construct_paginated_containers_list_response(item):
    return PaginatedContainersListResponse(
        data=[
            construct_cloud_insight_container(container) for container in item("data", [])
        ],
        total=item.get("total"),
        current_page=item.get("currentPage"),
        last_page=item.get("lastPage"),
    )
