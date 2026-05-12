from dataclasses import dataclass


@dataclass
class SpiInfoRepresentation:
    internal: ... = None
    providers: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "SpiInfoRepresentation":
        return cls(
            internal=item.get("internal"),
            providers=item.get("providers"),
        )
