from dataclasses import dataclass
from typing import Optional


@dataclass
class CxEngineServerStatus:

    status_id: Optional[int] = None
    value: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxEngineServerStatus":
        return cls(
            status_id=item.get("id"),
            value=item.get("value"),
        )
