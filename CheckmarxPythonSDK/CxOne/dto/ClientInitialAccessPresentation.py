from dataclasses import dataclass


@dataclass
class ClientInitialAccessPresentation:
    count: ... = None
    expiration: ... = None
    client_initial_access_presentation_id: ... = None
    remaining_count: ... = None
    timestamp: ... = None
    token: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientInitialAccessPresentation":
        return cls(
            count=item.get("count"),
            expiration=item.get("expiration"),
            client_initial_access_presentation_id=item.get("id"),
            remaining_count=item.get("remainingCount"),
            timestamp=item.get("timestamp"),
            token=item.get("token"),
        )
