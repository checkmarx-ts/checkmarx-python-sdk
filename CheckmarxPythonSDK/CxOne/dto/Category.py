from dataclasses import dataclass


@dataclass
class Category:
    id: int = None
    name: str = None
    sast_id: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "Category":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            sast_id=item.get("sastId"),
        )
