from dataclasses import dataclass
from typing import List


@dataclass
class Preset:
    """

    Args:
        id (int):
        name (str):
        description (str):
        custom (bool):
        query_ids (List[str])
    """
    id: str = None
    name: str = None
    description: str = None
    custom: bool = None
    query_ids: List[str] = None


def construct_preset(item):
    return Preset(
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        custom=item.get("custom"),
        query_ids=item.get("queryIds")
    )
