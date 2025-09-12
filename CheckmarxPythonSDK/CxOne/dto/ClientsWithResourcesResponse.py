from dataclasses import dataclass
from typing import List
from .ClientWithResource import construct_client_with_resource


@dataclass
class ClientsWithResourcesResponse:
    total_count: int = None
    filtered_count: int = None
    clients: List[dict] = None


def construct_clients_with_resources_response(item):
    return ClientsWithResourcesResponse(
        total_count=item.get("totalCount"),
        filtered_count=item.get("filteredCount"),
        clients=[
            construct_client_with_resource(client) for client in item.get("clients")
        ]
    )
