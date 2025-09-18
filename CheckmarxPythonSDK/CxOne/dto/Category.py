from dataclasses import dataclass


@dataclass
class Category:
    """
    Attributes:
        id (int):
        name (str):
        sast_id (int):

    """

    id: int = None
    name: str = None
    sast_id: int = None


def construct_category(item):
    return Category(
        id=item.get("id"),
        name=item.get("name"),
        sast_id=item.get("sastId")
    )
