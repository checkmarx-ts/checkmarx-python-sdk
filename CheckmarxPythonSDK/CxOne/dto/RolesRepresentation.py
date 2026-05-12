from dataclasses import dataclass


@dataclass
class RolesRepresentation:
    client: ... = None
    realm: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "RolesRepresentation":
        return cls(
            client=item.get("client"),
            realm=item.get("realm"),
        )
