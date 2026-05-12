from dataclasses import dataclass


@dataclass
class CustomState:
    id: int = None
    name: str = None
    type: str = None
    is_allowed: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "CustomState":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            type=item.get("type"),
            is_allowed=item.get("isAllowed"),
        )
