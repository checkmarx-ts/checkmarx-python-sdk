# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxLanguage:
    """
    the languages that Checkmarx supported
    """

    id: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxLanguage":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
        )
