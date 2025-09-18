from dataclasses import dataclass
from typing import List
from .Resource import Resource, construct_resource


@dataclass
class PaginatedResourcesList:
    data: List[Resource] = None
    total: int = None
    current_page: int = None
    last_page: int = None


def construct_paginated_resources_list(item):
    return PaginatedResourcesList(
        data=[
            construct_resource(resource) for resource in item.get("data", [])
        ],
        total=item.get("total"),
        current_page=item.get("currentPage"),
        last_page=item.get("lastPage"),
    )
