from dataclasses import dataclass


@dataclass
class ClientInitialAccessCreatePresentation:
    count: ... = None
    expiration: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientInitialAccessCreatePresentation":
        return cls(
            count=item.get("count"),
            expiration=item.get("expiration"),
        )
