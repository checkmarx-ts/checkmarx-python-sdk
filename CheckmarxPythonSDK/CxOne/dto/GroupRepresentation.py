from dataclasses import dataclass


@dataclass
class GroupRepresentation:
    id: str = None
    name: str = None
    path: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "GroupRepresentation":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            path=item.get("path"),
        )
