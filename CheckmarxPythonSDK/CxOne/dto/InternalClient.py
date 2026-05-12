from dataclasses import dataclass


@dataclass
class InternalClient:
    id: str = None
    client_id: str = None
    protocol: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "InternalClient":
        return cls(
            id=item.get("id"),
            client_id=item.get("clientId"),
            protocol=item.get("protocol"),
        )
