# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxTeam:
    """
    The team.
    """

    team_id: Optional[int] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    parent_id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxTeam":
        full_name = item.get("fullName") or ""
        return cls(
            team_id=item.get("id"),
            name=item.get("name"),
            full_name=full_name.replace("\\", "/"),
            parent_id=item.get("parentId"),
        )
