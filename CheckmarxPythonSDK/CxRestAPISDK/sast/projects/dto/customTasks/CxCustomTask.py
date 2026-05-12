# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxCustomTask:
    """
    custom tasks
    """

    id: Optional[int] = None
    name: Optional[str] = None
    custom_task_type: Optional[str] = None
    data: Optional[str] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxCustomTask":
        from ..CxLink import CxLink

        return cls(
            id=item.get("id"),
            name=item.get("name"),
            custom_task_type=item.get("type"),
            data=item.get("data"),
            link=CxLink.from_dict(item.get("link") or {}),
        )
