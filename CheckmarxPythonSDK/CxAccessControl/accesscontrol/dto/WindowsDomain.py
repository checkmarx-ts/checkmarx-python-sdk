from dataclasses import dataclass
from typing import Optional


@dataclass
class WindowsDomain:
    id: Optional[int] = None
    name: Optional[str] = None
    full_qualified_name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "WindowsDomain":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            full_qualified_name=item.get("fullyQualifiedName"),
        )
