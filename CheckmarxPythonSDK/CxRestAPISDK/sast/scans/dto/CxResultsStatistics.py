# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxResultsStatistics:
    """
    scan results statistics
    """

    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxResultsStatistics":
        return cls(
            link=item.get("link"),
        )
