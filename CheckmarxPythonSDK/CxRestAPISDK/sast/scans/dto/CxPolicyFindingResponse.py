# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxPolicyFindingResponse:
    """
    policy finding response
    """

    id: Optional[int] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxPolicyFindingResponse":
        return cls(
            id=item.get("id"),
            link=item.get("link"),
        )
