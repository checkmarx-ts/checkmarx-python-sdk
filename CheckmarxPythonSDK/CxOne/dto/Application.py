from dataclasses import dataclass
from typing import List
from .Rule import Rule, construct_rule


@dataclass
class Application:
    id: str = None
    name: str = None
    description: str = None
    criticality: int = None
    rules: List[Rule] = None
    project_ids: List[str] = None
    created_at: str = None
    updated_at: str = None
    tags: dict = None


def construct_application(item):
    return Application(
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        criticality=item.get("criticality"),
        rules=[
            construct_rule(rule) for rule in (item.get("rules") or [])
        ],
        project_ids=item.get("projectIds"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        tags=item.get("tags")
    )
