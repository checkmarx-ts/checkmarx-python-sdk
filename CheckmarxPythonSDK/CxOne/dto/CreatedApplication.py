from dataclasses import dataclass
from typing import List
from .Rule import Rule, construct_rule


@dataclass
class CreatedApplication:
    """

    Attributes:
        id (str):
        name (str):
        description (str):
        criticality (int):
        rules (`list` of `Rule`):
        tags (dict):
        created_at (str):
        updated_at (str):
    """

    id: str
    name: str
    description: str
    criticality: int
    rules: List[Rule]
    tags: dict
    created_at: str
    updated_at: str


def construct_created_application(item):
    return CreatedApplication(
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        criticality=item.get("criticality"),
        rules=[
            construct_rule(rule) for rule in (item.get("rules") or [])
        ],
        tags=item.get("tags"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt")
    )
