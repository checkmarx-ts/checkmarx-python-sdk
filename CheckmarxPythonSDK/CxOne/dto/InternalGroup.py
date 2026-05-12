from dataclasses import dataclass


@dataclass
class InternalGroup:
    id: str = None
    name: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "InternalGroup":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
        )
