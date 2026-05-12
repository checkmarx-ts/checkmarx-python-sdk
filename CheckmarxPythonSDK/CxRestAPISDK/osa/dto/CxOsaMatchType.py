# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxOsaMatchType:
    """
    match type
    """

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaMatchType":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
        )
