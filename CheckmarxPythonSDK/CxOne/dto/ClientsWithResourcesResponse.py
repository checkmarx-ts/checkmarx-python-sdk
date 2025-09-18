from dataclasses import dataclass
from typing import List
from .ClientWithResource import ClientWithResource, construct_client_with_resource


@dataclass
class ClientsWithResourcesResponse:
    total_count: int = None
    filtered_count: int = None
    clients: List[ClientWithResource] = None


def construct_clients_with_resources_response(item):
    return ClientsWithResourcesResponse(
        total_count=item.get("totalCount"),
        filtered_count=item.get("filteredCount"),
        clients=[
            construct_client_with_resource(client) for client in item.get("clients", [])
        ]
    )
