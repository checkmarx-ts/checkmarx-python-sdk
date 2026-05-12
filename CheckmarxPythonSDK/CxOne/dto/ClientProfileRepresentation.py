from dataclasses import dataclass


@dataclass
class ClientProfileRepresentation:
    description: ... = None
    executors: ... = None
    name: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientProfileRepresentation":
        return cls(
            description=item.get("description"),
            executors=item.get("executors"),
            name=item.get("name"),
        )
