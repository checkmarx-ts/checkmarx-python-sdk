from dataclasses import dataclass


@dataclass
class InternalClient:
    id: str = None
    client_id: str = None
    protocol: str = None


def construct_internal_client(item):
    return InternalClient(
        id=item.get("id"),
        client_id=item.get("clientId"),
        protocol=item.get("protocol"),
    )
