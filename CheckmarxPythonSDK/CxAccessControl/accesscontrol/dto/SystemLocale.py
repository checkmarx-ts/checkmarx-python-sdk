from dataclasses import dataclass
from typing import Optional


@dataclass
class SystemLocale:
    id: Optional[int] = None
    lcid: Optional[int] = None
    code: Optional[str] = None
    display_name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SystemLocale":
        return cls(
            id=item.get("id"),
            lcid=item.get("lcid"),
            code=item.get("code"),
            display_name=item.get("displayName"),
        )
