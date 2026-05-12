from dataclasses import dataclass


@dataclass
class Property:
    key: str = None
    value: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "Property":
        return cls(key=item.get("key"), value=item.get("value"))
