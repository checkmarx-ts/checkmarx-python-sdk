from dataclasses import dataclass
from .Category import Category, construct_category
from typing import List


@dataclass
class CategoryType:

    """
    Attributes:
        id (int):
        name (str):
        sast_id (int):
        order (int):
        categories (list of Category):
    """
    id: int = None
    name: str = None
    sast_id: int = None
    order: int = None
    categories: List[Category] = None


def construct_category_type(item):
    return CategoryType(
        id=item.get("id"),
        name=item.get("name"),
        sast_id=item.get("sastId"),
        order=item.get("order"),
        categories=[
            construct_category(category) for category in item.get("categories", [])
        ]
    )
