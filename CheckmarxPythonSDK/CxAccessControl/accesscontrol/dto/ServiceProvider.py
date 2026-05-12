from dataclasses import dataclass
from typing import Optional


@dataclass
class ServiceProvider:
    id: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ServiceProvider":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
        )
