from dataclasses import dataclass
from .Category import Category
from typing import List


@dataclass
class CategoryType:
    id: int = None
    name: str = None
    sast_id: int = None
    order: int = None
    categories: List[Category] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CategoryType":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            sast_id=item.get("sastId"),
            order=item.get("order"),
            categories=[Category.from_dict(c) for c in (item.get("categories") or [])],
        )
