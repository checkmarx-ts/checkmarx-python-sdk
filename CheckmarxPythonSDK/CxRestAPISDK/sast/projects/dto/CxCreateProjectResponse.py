# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxCreateProjectResponse:
    """
    the response data, when create a project
    """

    id: Optional[int] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxCreateProjectResponse":
        from .CxLink import CxLink

        return cls(
            id=item.get("id"),
            link=CxLink.from_dict(item.get("link") or {}),
        )
