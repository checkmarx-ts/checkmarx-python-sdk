# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxLink:
    """
    the link information of a project
    """

    rel: Optional[str] = None
    uri: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxLink":
        return cls(
            rel=item.get("rel"),
            uri=item.get("uri"),
        )
