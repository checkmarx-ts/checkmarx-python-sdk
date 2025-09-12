from dataclasses import dataclass
from typing import List
from .Rule import Rule


@dataclass
class Application:
    application_id: str = None
    name: str = None
    description: str = None
    criticality: int = None
    rules: List[Rule] = None
    project_ids: List[str] = None
    created_at: str = None
    updated_at: str = None
    tags: dict = None


def construct_application_rules(rules) -> List[Rule]:
    rules = rules or []
    return [
        Rule(
            rule_id=rule.get("id"),
            rule_type=rule.get("type"),
            value=rule.get("value")
        ) for rule in rules
    ]


def construct_application(item):
    return Application(
        application_id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        criticality=item.get("criticality"),
        rules=construct_application_rules(item.get("rules")),
        project_ids=item.get("projectIds"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        tags=item.get("tags")
    )
