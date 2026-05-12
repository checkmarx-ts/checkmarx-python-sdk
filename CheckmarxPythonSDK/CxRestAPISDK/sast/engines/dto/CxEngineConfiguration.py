# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxEngineConfiguration:
    """
    engine configuration
    """

    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxEngineConfiguration":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            link=item.get("link"),
        )
