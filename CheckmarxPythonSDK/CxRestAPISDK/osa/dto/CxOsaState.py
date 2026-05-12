# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxOsaState:
    """
    state
    """

    id: Optional[int] = None
    name: Optional[str] = None
    failure_reason: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaState":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            failure_reason=item.get("failureReason"),
        )
