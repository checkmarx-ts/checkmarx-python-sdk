from dataclasses import dataclass


@dataclass
class KeysMetadataRepresentation:
    active: ... = None
    keys: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "KeysMetadataRepresentation":
        return cls(
            active=item.get("active"),
            keys=item.get("keys"),
        )
