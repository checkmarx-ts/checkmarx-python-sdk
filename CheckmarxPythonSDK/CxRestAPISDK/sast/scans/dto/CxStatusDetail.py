# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxStatusDetail:
    """
    scan status detail
    """

    stage: Optional[str] = None
    step: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxStatusDetail":
        return cls(
            stage=item.get("stage"),
            step=item.get("step"),
        )
